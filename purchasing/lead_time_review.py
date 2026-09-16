"""The weekly purchasing review, done by something that never skips a line.

Why this exists (Josh, 2026-09-16):

  The failure is never "nobody fixed the purchasing problem". It is that the
  ask gets broad, somebody fixes the one part that screamed, and nobody looks
  at *why* it screamed. The expensive version: a PO goes in that violates the
  supplier's lead time, it sits in the system looking fine because it has a due
  date, and the first person to notice is the supplier -- on the day it was
  due, saying "you violated lead time, you will have it in four weeks."

So this does not send an alert. It produces the packet for a sit-down review,
and it can say honestly, every week:

    I looked at every lead time, every open order, and every order date.

Four things get checked against each other, per part:

  1. **Lead time vs. the order date.** An open PO's real arrival is
     `order_date + lead_time`, not whatever due date was typed. Where those
     disagree, the due date is fiction and the review says so *now* rather than
     on the due date.
  2. **Current on hand.**
  3. **Current demand, at full** -- every dated requirement, not net of
     whatever somebody already decided to ignore.
  4. **Box quantity.** If it ships in boxes of 5,000 and the system says 1,200,
     you have one full box you can trust and a partial box you cannot. The
     partial is the one that turns out to hold 200. So every part is projected
     twice: once on the number in the system, once discounting the open box
     entirely. A part that only survives on the partial box is a part to go
     count, not a part that is fine.

Run it:

    python lead_time_review.py --data sample-data --out reviews/2026-09-21.md
    python lead_time_review.py --data ~/exports --asof 2026-09-21 --findings out.csv

Input is three CSVs -- `parts.csv`, `open_pos.csv`, `demand.csv`. Column names
come from `source-map.json`, so pointing this at a different ERP export is an
edit to that file, not to this one. See README.md for the contract.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent

# Severity drives the order of the packet. The review is read top-down and the
# top is meant to be the part where money is already leaking.
CRITICAL, HIGH, MEDIUM, DATA = "critical", "high", "medium", "data"
SEVERITY_RANK = {CRITICAL: 0, HIGH: 1, MEDIUM: 2, DATA: 3}

DATE_FORMATS = ("%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y", "%d-%b-%Y", "%Y/%m/%d", "%m-%d-%Y")


def die(msg: str) -> None:
    sys.exit(f"error: {msg}")


def parse_date(raw: str | None) -> date | None:
    """ERP exports disagree about dates; none of them are worth failing over."""
    if not raw:
        return None
    raw = raw.strip()
    if not raw:
        return None
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(raw, fmt).date()
        except ValueError:
            continue
    return None


def parse_num(raw: str | None) -> float | None:
    """Tolerate `1,200`, `$1200.00`, `(50)` for negative, and blank."""
    if raw is None:
        return None
    s = str(raw).strip().replace(",", "").replace("$", "")
    if not s:
        return None
    negative = s.startswith("(") and s.endswith(")")
    if negative:
        s = s[1:-1]
    try:
        value = float(s)
    except ValueError:
        return None
    return -value if negative else value


# --------------------------------------------------------------------------
# The three inputs
# --------------------------------------------------------------------------

@dataclass
class Part:
    part: str
    description: str = ""
    supplier: str = ""
    lead_time_days: int | None = None
    box_qty: float | None = None
    on_hand: float = 0.0
    safety_stock: float = 0.0
    uom: str = ""

    @property
    def trusted_on_hand(self) -> float:
        """On hand with the open box thrown away.

        Josh's rule, and the reason it is the default rather than a warning:
        the partial box is the only quantity nobody ever verified. A full box
        is sealed and countable at a glance. So whole boxes are believed and
        the remainder is not, which means a part sitting below one box is
        treated as **zero** until somebody physically counts it.
        """
        if not self.box_qty or self.box_qty <= 0:
            return self.on_hand
        if self.on_hand <= 0:
            return self.on_hand
        return math.floor(self.on_hand / self.box_qty) * self.box_qty

    @property
    def open_box_qty(self) -> float:
        if not self.box_qty or self.box_qty <= 0 or self.on_hand <= 0:
            return 0.0
        return self.on_hand - self.trusted_on_hand


@dataclass
class PurchaseOrder:
    po: str
    part: str
    qty: float
    order_date: date | None
    due_date: date | None
    line: str = ""
    supplier: str = ""

    @property
    def ref(self) -> str:
        return f"{self.po}-{self.line}" if self.line else self.po

    def earliest_possible(self, lead_time_days: int | None) -> date | None:
        """The first day the supplier could physically deliver it.

        This is the whole point: it is measured from the day the order was
        placed, not from the day somebody wanted it.
        """
        if self.order_date is None or lead_time_days is None:
            return None
        return self.order_date + timedelta(days=lead_time_days)

    def slip_days(self, lead_time_days: int | None) -> int:
        """How many days the due date is inside the lead time. 0 means honest."""
        earliest = self.earliest_possible(lead_time_days)
        if earliest is None or self.due_date is None:
            return 0
        return max(0, (earliest - self.due_date).days)

    def expected_arrival(self, lead_time_days: int | None, asof: date) -> date | None:
        """When it actually shows up, believing lead time over the due date.

        Three claims, and we take the latest: the typed due date, lead time
        from the order date, and today (a PO that is past due and has not
        arrived is not going to arrive in the past).
        """
        claims = [d for d in (self.due_date, self.earliest_possible(lead_time_days)) if d]
        if not claims:
            return None
        return max(max(claims), asof)


@dataclass
class DemandLine:
    part: str
    qty: float
    need_date: date | None
    source: str = ""
    ref: str = ""


@dataclass
class Finding:
    severity: str
    code: str
    part: str
    headline: str
    detail: list[str] = field(default_factory=list)
    action: str = ""

    def sort_key(self) -> tuple:
        return (SEVERITY_RANK.get(self.severity, 9), self.code, self.part)


# --------------------------------------------------------------------------
# Loading
# --------------------------------------------------------------------------

def load_map(path: Path) -> dict:
    if not path.exists():
        die(f"no column map at {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def read_rows(path: Path, mapping: dict[str, str]) -> list[dict[str, str]]:
    """Read a CSV and rename its columns to our canonical names.

    Matching ignores case and surrounding whitespace, because ERP exports
    capitalise headers however they feel that day.
    """
    if not path.exists():
        die(f"missing input file: {path}")
    with path.open(newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames is None:
            die(f"{path.name} has no header row")
        lookup = {(h or "").strip().lower(): h for h in reader.fieldnames}
        resolved: dict[str, str] = {}
        for canonical, source in mapping.items():
            header = lookup.get(source.strip().lower())
            if header is not None:
                resolved[canonical] = header
        rows = []
        for raw in reader:
            rows.append({k: (raw.get(h) or "").strip() for k, h in resolved.items()})
        return rows


def load_parts(data: Path, colmap: dict) -> dict[str, Part]:
    parts: dict[str, Part] = {}
    for row in read_rows(data / "parts.csv", colmap["parts"]):
        number = row.get("part", "")
        if not number:
            continue
        lead = parse_num(row.get("lead_time_days"))
        parts[number] = Part(
            part=number,
            description=row.get("description", ""),
            supplier=row.get("supplier", ""),
            lead_time_days=int(lead) if lead is not None else None,
            box_qty=parse_num(row.get("box_qty")),
            on_hand=parse_num(row.get("on_hand")) or 0.0,
            safety_stock=parse_num(row.get("safety_stock")) or 0.0,
            uom=row.get("uom", ""),
        )
    return parts


def load_pos(data: Path, colmap: dict) -> list[PurchaseOrder]:
    orders = []
    for row in read_rows(data / "open_pos.csv", colmap["open_pos"]):
        if not row.get("part"):
            continue
        orders.append(PurchaseOrder(
            po=row.get("po", ""),
            line=row.get("line", ""),
            part=row["part"],
            qty=parse_num(row.get("qty")) or 0.0,
            order_date=parse_date(row.get("order_date")),
            due_date=parse_date(row.get("due_date")),
            supplier=row.get("supplier", ""),
        ))
    return orders


def load_demand(data: Path, colmap: dict) -> list[DemandLine]:
    lines = []
    for row in read_rows(data / "demand.csv", colmap["demand"]):
        if not row.get("part"):
            continue
        lines.append(DemandLine(
            part=row["part"],
            qty=parse_num(row.get("qty")) or 0.0,
            need_date=parse_date(row.get("need_date")),
            source=row.get("source", ""),
            ref=row.get("ref", ""),
        ))
    return lines


# --------------------------------------------------------------------------
# The projection
# --------------------------------------------------------------------------

@dataclass
class Projection:
    """A part's dated balance, walked forward from today."""
    shortage_date: date | None = None
    shortage_qty: float = 0.0
    ending_balance: float = 0.0
    total_demand: float = 0.0
    total_incoming: float = 0.0


def project(start_qty: float, part: Part, receipts: list[tuple[date, float]],
            requirements: list[tuple[date, float]]) -> Projection:
    """Walk the balance through every dated event and find the first hole.

    Same-day ties go to the requirement, not the receipt. A truck that arrives
    the morning it is needed is a coin flip, and this review is not in the
    business of calling coin flips fine.
    """
    events: list[tuple[date, int, float]] = []
    for when, qty in requirements:
        events.append((when, 0, -qty))
    for when, qty in receipts:
        events.append((when, 1, qty))
    events.sort(key=lambda e: (e[0], e[1]))

    result = Projection(
        total_demand=sum(q for _, q in requirements),
        total_incoming=sum(q for _, q in receipts),
    )
    balance = start_qty
    for when, _, delta in events:
        balance += delta
        if result.shortage_date is None and balance < part.safety_stock:
            result.shortage_date = when
            result.shortage_qty = part.safety_stock - balance
    result.ending_balance = balance
    return result


def order_by(shortage: date | None, lead_time_days: int | None) -> date | None:
    """The last day you could place the order and still be on time."""
    if shortage is None or lead_time_days is None:
        return None
    return shortage - timedelta(days=lead_time_days)


def round_to_box(qty: float, box_qty: float | None) -> float:
    """Never order a partial box -- you will be short-shipped or rounded anyway."""
    if not box_qty or box_qty <= 0:
        return math.ceil(qty)
    return math.ceil(qty / box_qty) * box_qty


def fmt_qty(qty: float) -> str:
    return f"{qty:,.0f}" if float(qty).is_integer() else f"{qty:,.2f}"


def fmt_date(when: date | None) -> str:
    return when.isoformat() if when else "—"


def days_word(n: int) -> str:
    return f"{n} day" if abs(n) == 1 else f"{n} days"


# --------------------------------------------------------------------------
# The checks
# --------------------------------------------------------------------------

@dataclass
class PartReview:
    part: Part
    pos: list[PurchaseOrder]
    demand: list[DemandLine]
    nominal: Projection
    trusted: Projection
    status: str
    order_by_date: date | None
    suggested_qty: float


def review_part(part: Part, pos: list[PurchaseOrder], demand: list[DemandLine],
                asof: date, horizon: date) -> tuple[PartReview, list[Finding]]:
    findings: list[Finding] = []
    lead = part.lead_time_days
    label = f"`{part.part}`" + (f" — {part.description}" if part.description else "")

    # --- Data gaps first. Every check below is a lie without these. ---------
    if lead is None or lead <= 0:
        findings.append(Finding(
            DATA, "NO-LEAD-TIME", part.part,
            f"{label} has no usable lead time"
            + (f" (`{lead}`)" if lead is not None else ""),
            ["Every lead-time test on this part is skipped, so it passes this review by "
             "default. That is exactly how a part goes quiet until the supplier calls — "
             "nothing here can tell you when to order it."],
            action=f"Get the real lead time from {part.supplier or 'the supplier'} and put it in the item master.",
        ))
    if not part.box_qty or part.box_qty <= 0:
        findings.append(Finding(
            DATA, "NO-BOX-QTY", part.part,
            f"{label} has no box quantity",
            ["On hand is taken at face value and order quantities are not rounded, so "
             "partial-box error cannot be detected on this part."],
            action="Record the purchase multiple (box, reel, case) on the item.",
        ))
    if part.on_hand < 0:
        findings.append(Finding(
            DATA, "NEGATIVE-ON-HAND", part.part,
            f"{label} shows negative on hand ({fmt_qty(part.on_hand)})",
            ["A negative balance means issues were posted against stock that was never "
             "received. The count is wrong, not the demand."],
            action="Reconcile before ordering against this number.",
        ))

    # --- Open POs: does the due date survive the lead time? -----------------
    receipts: list[tuple[date, float]] = []
    for po in pos:
        arrival = po.expected_arrival(lead, asof)
        if arrival is not None:
            receipts.append((arrival, po.qty))

        if po.order_date is None:
            findings.append(Finding(
                DATA, "PO-NO-ORDER-DATE", part.part,
                f"{label} — PO {po.ref} has no order date",
                ["Without the order date there is nothing to measure lead time from, so "
                 "this PO's due date cannot be checked at all."],
                action="Fill in the order date, then re-run.",
            ))
            continue

        slip = po.slip_days(lead)
        if slip > 0:
            earliest = po.earliest_possible(lead)
            findings.append(Finding(
                CRITICAL if slip >= 7 else HIGH, "LEAD-TIME-VIOLATED", part.part,
                f"{label} — PO {po.ref} was placed inside its own lead time, "
                f"by {days_word(slip)}",
                [f"Ordered {fmt_date(po.order_date)}, due {fmt_date(po.due_date)}, "
                 f"lead time {lead} days.",
                 f"Earliest the supplier can deliver is {fmt_date(earliest)}.",
                 f"The due date in the system is {days_word(slip)} earlier than that, so it is not real.",
                 "Nothing looks wrong today. It goes wrong on the due date, when the "
                 "supplier quotes the job from scratch."],
                action=(f"Call {po.supplier or part.supplier or 'the supplier'} now and get a committed date "
                        f"while there is still time to plan around it — or pay to expedite. "
                        f"Do not wait for {fmt_date(po.due_date)}."),
            ))
        elif po.due_date and po.due_date < asof:
            findings.append(Finding(
                HIGH, "PO-PAST-DUE", part.part,
                f"{label} — PO {po.ref} is {days_word((asof - po.due_date).days)} past due",
                [f"Ordered {fmt_date(po.order_date)}, was due {fmt_date(po.due_date)}, "
                 f"still open for {fmt_qty(po.qty)}{' ' + part.uom if part.uom else ''}.",
                 "Lead time was respected when it was placed, so this is a supplier miss, "
                 "not an ordering mistake."],
                action=f"Chase {po.supplier or part.supplier or 'the supplier'} for a new committed date.",
            ))

        if part.box_qty and part.box_qty > 0 and po.qty > 0:
            remainder = po.qty % part.box_qty
            if remainder:
                findings.append(Finding(
                    MEDIUM, "PO-NOT-BOX-MULTIPLE", part.part,
                    f"{label} — PO {po.ref} orders {fmt_qty(po.qty)}, "
                    f"not a multiple of the {fmt_qty(part.box_qty)} box",
                    [f"Expect either {fmt_qty(po.qty - remainder)} (short) or "
                     f"{fmt_qty(round_to_box(po.qty, part.box_qty))} (rounded up).",
                     "If the plan assumed the exact number, it is already wrong by "
                     f"{fmt_qty(remainder)}."],
                    action=f"Confirm what the supplier will actually ship, or change the line to "
                           f"{fmt_qty(round_to_box(po.qty, part.box_qty))}.",
                ))

    requirements = [(d.need_date, d.qty) for d in demand if d.need_date]
    for line in demand:
        if line.need_date is None:
            findings.append(Finding(
                DATA, "DEMAND-NO-DATE", part.part,
                f"{label} — demand {line.ref or line.source or '(unlabelled)'} "
                f"for {fmt_qty(line.qty)} has no date",
                ["Undated demand is invisible to the projection below. It is real material "
                 "somebody expects, and it is not in the numbers."],
                action="Date it, or confirm it is dead and close it.",
            ))

    nominal = project(part.on_hand, part, receipts, requirements)
    trusted = project(part.trusted_on_hand, part, receipts, requirements)

    # If a shortage is already going to be reported, the open box belongs in that
    # finding as a bigger number -- not as a second finding about the same part.
    box_note: list[str] = []
    if part.open_box_qty > 0 and trusted.shortage_qty > nominal.shortage_qty:
        if part.trusted_on_hand <= 0:
            held = (f"None of the {fmt_qty(part.on_hand)} on hand is in a sealed box — the whole "
                    f"balance is one open box.")
        else:
            held = (f"Only {fmt_qty(part.trusted_on_hand)} of the {fmt_qty(part.on_hand)} on hand "
                    f"is in sealed boxes; {fmt_qty(part.open_box_qty)} is loose in an open box.")
        box_note = [
            held + f" If that count is off, the shortfall is {fmt_qty(trusted.shortage_qty)}, not "
                   f"{fmt_qty(nominal.shortage_qty)} — so order "
                   f"{fmt_qty(round_to_box(trusted.shortage_qty, part.box_qty))} and count it."
        ]

    # --- Coverage: is the hole reachable, and when must the order go? ------
    status = "ok"
    ob = order_by(nominal.shortage_date, lead)
    suggested = 0.0

    if nominal.shortage_date is not None:
        suggested = round_to_box(nominal.shortage_qty, part.box_qty)
        qty_text = f"{fmt_qty(suggested)}{' ' + part.uom if part.uom else ''}"
        if ob is not None and ob < asof:
            status = "late"
            late_by = (asof - ob).days
            findings.append(Finding(
                CRITICAL, "ALREADY-LATE", part.part,
                f"{label} runs out {fmt_date(nominal.shortage_date)} and the order "
                f"was due {days_word(late_by)} ago",
                [f"Short {fmt_qty(nominal.shortage_qty)} on {fmt_date(nominal.shortage_date)}.",
                 f"Lead time is {lead} days, so the last honest order date was {fmt_date(ob)}.",
                 "Ordering today does not fix this. An order placed today lands "
                 f"{fmt_date(asof + timedelta(days=lead))}.",
                 "This is the one that becomes a lead-time violation if it is entered as if "
                 "it were not."] + box_note,
                action=f"Expedite, split the order, or move the job. Order {qty_text} today regardless, "
                       f"and tell the floor the real date — do not enter a due date the supplier never agreed to.",
            ))
        elif ob is not None and ob <= horizon:
            status = "order-now"
            findings.append(Finding(
                HIGH, "ORDER-NOW", part.part,
                f"{label} must be ordered by {fmt_date(ob)}",
                [f"Runs short {fmt_qty(nominal.shortage_qty)} on {fmt_date(nominal.shortage_date)}.",
                 f"Lead time {lead} days. On hand {fmt_qty(part.on_hand)}, "
                 f"incoming {fmt_qty(nominal.total_incoming)}, demand {fmt_qty(nominal.total_demand)}.",
                 "That date is inside this review's window, so it will not survive until "
                 "the next one."] + box_note,
                action=f"Place {qty_text} on {part.supplier or 'the supplier'} before {fmt_date(ob)}.",
            ))
        elif ob is None:
            status = "unknown"
            findings.append(Finding(
                HIGH, "SHORT-NO-LEAD-TIME", part.part,
                f"{label} runs short on {fmt_date(nominal.shortage_date)} and has no lead time",
                [f"Short {fmt_qty(nominal.shortage_qty)}. Without a lead time there is no way "
                 "to say when the order has to go, so it cannot be scheduled."],
                action="Get the lead time, then re-run. Until then treat it as order-today.",
            ))
        else:
            status = "watch"

    # --- Box quantity: the part that is only fine because of an open box ---
    # Two distinct failures, and the first is the one that bites hardest: the
    # part reads as covered, right up until somebody opens the box.
    if part.box_qty and part.box_qty > 0 and part.open_box_qty > 0:
        hidden_shortage = (
            nominal.shortage_date is None and trusted.shortage_date is not None)
        # Only when the open box moves the *date*, which moves the action. A bigger
        # quantity on the same date is already said in box_note above.
        deeper_shortage = (
            nominal.shortage_date is not None and trusted.shortage_date is not None
            and trusted.shortage_date < nominal.shortage_date)

        if hidden_shortage or deeper_shortage:
            t_ob = order_by(trusted.shortage_date, lead)
            no_full_box = part.on_hand < part.box_qty
            severity = CRITICAL if (hidden_shortage or no_full_box) else HIGH

            if hidden_shortage:
                headline = f"{label} looks covered, and is only covered by an open box"
            else:
                headline = f"{label} is shorter than it looks — the open box is propping it up"

            detail = [
                f"System says {fmt_qty(part.on_hand)} on hand: "
                f"{fmt_qty(part.trusted_on_hand)} in whole boxes plus "
                f"{fmt_qty(part.open_box_qty)} loose in an open box.",
            ]
            if hidden_shortage:
                detail.append(
                    f"On the system number this part never goes short. Counting only sealed "
                    f"boxes it goes short {fmt_qty(trusted.shortage_qty)} on "
                    f"{fmt_date(trusted.shortage_date)}.")
            else:
                detail.append(
                    f"On the system number it goes short {fmt_qty(nominal.shortage_qty)} on "
                    f"{fmt_date(nominal.shortage_date)}. Counting only sealed boxes it is "
                    f"{fmt_qty(trusted.shortage_qty)} short on {fmt_date(trusted.shortage_date)}.")
            detail.append(
                f"Either way the plan is resting on {fmt_qty(part.open_box_qty)} that nobody "
                f"has counted.")
            if no_full_box:
                detail.append(
                    f"There is not one full box here — the entire balance is an open box. This "
                    f"is the case that gets people: the box you believe holds "
                    f"{fmt_qty(part.on_hand)} is the box that turns out to hold a fraction of it.")
            if t_ob is not None:
                detail.append(
                    f"If the count is wrong, the order was due {fmt_date(t_ob)}"
                    + (" — already past." if t_ob < asof else "."))

            findings.append(Finding(
                severity, "PARTIAL-BOX-RISK", part.part, headline, detail,
                action=f"Physically count {part.part} before the review and correct the balance, "
                       f"then re-run. Do not plan off the open box.",
            ))
            if status == "ok":
                status = "count-it"

    review = PartReview(
        part=part, pos=pos, demand=demand, nominal=nominal, trusted=trusted,
        status=status, order_by_date=ob, suggested_qty=suggested,
    )
    return review, findings


# --------------------------------------------------------------------------
# The packet
# --------------------------------------------------------------------------

SECTIONS = [
    ("Act today", [
        ("ALREADY-LATE", "Past the last honest order date"),
        ("LEAD-TIME-VIOLATED", "Open orders placed inside their own lead time"),
    ]),
    ("Order this week", [
        ("ORDER-NOW", "The order-by date falls inside this review's window"),
        ("SHORT-NO-LEAD-TIME", "Short, and no lead time to schedule it from"),
    ]),
    ("Count before you trust it", [
        ("PARTIAL-BOX-RISK", "Covered only by an open box, or short sooner than it looks"),
    ]),
    ("Chase the supplier", [
        ("PO-PAST-DUE", "Open orders past their due date"),
        ("PO-NOT-BOX-MULTIPLE", "Order quantities that are not whole boxes"),
    ]),
    ("Fix the data — these parts pass by default", [
        ("NO-LEAD-TIME", "No usable lead time"),
        ("NO-BOX-QTY", "No box quantity"),
        ("NEGATIVE-ON-HAND", "Negative on-hand balance"),
        ("PO-NO-ORDER-DATE", "Open order with no order date"),
        ("DEMAND-NO-DATE", "Demand with no date"),
        ("UNKNOWN-PART", "Orders or demand against a part that is not in the item master"),
    ]),
]

STATUS_LABEL = {
    "ok": "OK",
    "watch": "Watch",
    "count-it": "Count it",
    "order-now": "Order now",
    "late": "LATE",
    "unknown": "No lead time",
}


def render(reviews: list[PartReview], findings: list[Finding], asof: date,
           horizon_days: int, po_count: int, demand_count: int) -> str:
    out: list[str] = []
    w = out.append

    by_code: dict[str, list[Finding]] = {}
    for f in findings:
        by_code.setdefault(f.code, []).append(f)

    parts_flagged = {f.part for f in findings}
    criticals = [f for f in findings if f.severity == CRITICAL]

    w(f"# Purchasing review — {asof.isoformat()}")
    w("")
    w("Read top-down. The top of this packet is where money is already leaking; the bottom")
    w("is where the next one will leak from.")
    w("")

    # The ledger. This is the claim the meeting is supposed to be able to make.
    w("## What was checked")
    w("")
    w("| Looked at | Count |")
    w("| --- | ---: |")
    w(f"| Parts | {len(reviews)} |")
    w(f"| Lead times | {sum(1 for r in reviews if r.part.lead_time_days)} of {len(reviews)} |")
    w(f"| Open purchase order lines | {po_count} |")
    w(f"| Order dates on those lines | {sum(1 for r in reviews for p in r.pos if p.order_date)} of {po_count} |")
    w(f"| Dated demand lines | {demand_count} |")
    w(f"| Parts with a box quantity | {sum(1 for r in reviews if r.part.box_qty)} of {len(reviews)} |")
    w("")
    w(f"Every part above was projected twice — once on the on-hand number in the system, once")
    w(f"with the open box discounted. The order-by window for this review is {horizon_days} days.")
    w("")
    if criticals:
        w(f"**{len(criticals)} critical, {len(findings)} findings across {len(parts_flagged)} parts.**")
    else:
        w(f"**No critical findings. {len(findings)} findings across {len(parts_flagged)} parts.**")
    w("")

    for title, codes in SECTIONS:
        present = [(code, blurb) for code, blurb in codes if by_code.get(code)]
        if not present:
            continue
        w(f"## {title}")
        w("")
        for code, blurb in present:
            items = sorted(by_code[code], key=lambda f: f.sort_key())
            w(f"### {blurb} ({len(items)})")
            w("")
            for f in items:
                w(f"- **{f.headline}**")
                for line in f.detail:
                    w(f"  - {line}")
                if f.action:
                    w(f"  - *Do:* {f.action}")
            w("")

    # A finding with no home in SECTIONS would otherwise be generated and never
    # printed, which is the one failure mode this packet cannot have.
    homed = {code for _, codes in SECTIONS for code, _ in codes}
    stray = sorted(set(by_code) - homed)
    if stray:
        w("## Other findings")
        w("")
        for code in stray:
            for f in sorted(by_code[code], key=lambda f: f.sort_key()):
                w(f"- **{f.headline}** ({code})")
                for line in f.detail:
                    w(f"  - {line}")
                if f.action:
                    w(f"  - *Do:* {f.action}")
        w("")

    # Full coverage. Every part gets a line whether or not it had a finding,
    # because "I looked at every one" is the claim, and a list of only the
    # problems cannot support it.
    w("## Every part, and where it stands")
    w("")
    w("| Part | Lead time | On hand | Trusted | Incoming | Demand | Short on | Order by | Status |")
    w("| --- | ---: | ---: | ---: | ---: | ---: | --- | --- | --- |")
    order = {"late": 0, "order-now": 1, "unknown": 2, "count-it": 3, "watch": 4, "ok": 5}
    for r in sorted(reviews, key=lambda r: (order.get(r.status, 9), r.part.part)):
        p = r.part
        trusted = fmt_qty(p.trusted_on_hand) + ("" if p.trusted_on_hand == p.on_hand else " ⚠")
        w(f"| `{p.part}` "
          f"| {p.lead_time_days if p.lead_time_days is not None else '—'} "
          f"| {fmt_qty(p.on_hand)} "
          f"| {trusted} "
          f"| {fmt_qty(r.nominal.total_incoming)} "
          f"| {fmt_qty(r.nominal.total_demand)} "
          f"| {fmt_date(r.nominal.shortage_date)} "
          f"| {fmt_date(r.order_by_date)} "
          f"| {STATUS_LABEL.get(r.status, r.status)} |")
    w("")
    w("*Trusted* is on hand with the open box discounted — whole boxes only. A ⚠ means the")
    w("two numbers disagree, which means part of that balance has never been counted.")
    w("")
    w("---")
    w("")
    w("Generated by `purchasing/lead_time_review.py`. This packet is the agenda, not the minutes —")
    w("every line under *Act today* needs a name and a date against it before the meeting ends.")
    w("")
    return "\n".join(out)


def write_findings_csv(path: Path, findings: list[Finding]) -> None:
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["severity", "code", "part", "headline", "detail", "action"])
        for f in sorted(findings, key=lambda f: f.sort_key()):
            writer.writerow([f.severity, f.code, f.part, f.headline, " ".join(f.detail), f.action])


# --------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--data", type=Path, default=HERE / "sample-data",
                    help="folder holding parts.csv, open_pos.csv, demand.csv")
    ap.add_argument("--map", type=Path, default=HERE / "source-map.json",
                    help="column map from your export's headers to ours")
    ap.add_argument("--asof", default=None, help="review date (default: today)")
    ap.add_argument("--horizon", type=int, default=7,
                    help="days ahead an order-by date counts as this week's work")
    ap.add_argument("--out", type=Path, default=None, help="write the packet here")
    ap.add_argument("--findings", type=Path, default=None, help="also write findings as CSV")
    args = ap.parse_args()

    asof = parse_date(args.asof) if args.asof else date.today()
    if asof is None:
        die(f"could not read --asof {args.asof!r}")
    horizon = asof + timedelta(days=args.horizon)

    colmap = load_map(args.map)
    parts = load_parts(args.data, colmap)
    if not parts:
        die(f"no parts loaded from {args.data / 'parts.csv'} — check source-map.json")
    pos = load_pos(args.data, colmap)
    demand = load_demand(args.data, colmap)

    pos_by_part: dict[str, list[PurchaseOrder]] = {}
    for po in pos:
        pos_by_part.setdefault(po.part, []).append(po)
    demand_by_part: dict[str, list[DemandLine]] = {}
    for line in demand:
        demand_by_part.setdefault(line.part, []).append(line)

    reviews: list[PartReview] = []
    findings: list[Finding] = []

    # A PO or a demand line for a part that is not in the item master is
    # invisible to every check, so it gets said out loud rather than dropped.
    orphans = (set(pos_by_part) | set(demand_by_part)) - set(parts)
    for orphan in sorted(orphans):
        findings.append(Finding(
            DATA, "UNKNOWN-PART", orphan,
            f"`{orphan}` has orders or demand but is not in the item master",
            ["No lead time, no box quantity, no on-hand — so it is not reviewed at all."],
            action="Add it to the item master, or correct the part number on those lines.",
        ))

    for number in sorted(parts):
        review, part_findings = review_part(
            parts[number], pos_by_part.get(number, []), demand_by_part.get(number, []),
            asof, horizon)
        reviews.append(review)
        findings.extend(part_findings)

    packet = render(reviews, findings, asof, args.horizon, len(pos), len(demand))

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(packet, encoding="utf-8")
        print(f"wrote {args.out}")
    else:
        print(packet)

    if args.findings:
        write_findings_csv(args.findings, findings)
        print(f"wrote {args.findings}")

    criticals = sum(1 for f in findings if f.severity == CRITICAL)
    if args.out:
        print(f"{len(findings)} findings, {criticals} critical, across {len(reviews)} parts")
    return 1 if criticals else 0


if __name__ == "__main__":
    raise SystemExit(main())
