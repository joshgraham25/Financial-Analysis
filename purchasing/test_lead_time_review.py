"""Pin the arithmetic the review depends on. `python test_lead_time_review.py`.

These are the four claims the packet makes every week. If one of them breaks,
the review keeps producing a confident-looking document that is wrong, which is
worse than producing nothing -- so they are tested rather than eyeballed.
"""

from __future__ import annotations

import subprocess
import sys
from datetime import date
from pathlib import Path

from lead_time_review import (
    DemandLine, Part, PurchaseOrder, parse_date, parse_num, project,
    review_part, order_by, round_to_box,
)

HERE = Path(__file__).resolve().parent
ASOF = date(2026, 9, 16)
FAILURES: list[str] = []


def check(label: str, got, want) -> None:
    if got != want:
        FAILURES.append(f"{label}: got {got!r}, want {want!r}")


def codes(findings) -> set[str]:
    return {f.code for f in findings}


def run(part: Part, pos=(), demand=(), horizon_days: int = 7):
    return review_part(part, list(pos), list(demand), ASOF,
                       date.fromordinal(ASOF.toordinal() + horizon_days))


# --- 1. A due date inside the lead time is caught at review, not at the due date.
po = PurchaseOrder(po="P-1", part="A", qty=100,
                   order_date=date(2026, 9, 11), due_date=date(2026, 9, 18))
check("slip days", po.slip_days(14), 7)
check("earliest possible", po.earliest_possible(14), date(2026, 9, 25))
check("arrival believes lead time over due date",
      po.expected_arrival(14, ASOF), date(2026, 9, 25))
_, found = run(Part("A", lead_time_days=14, box_qty=100, on_hand=500), [po])
check("violation reported", "LEAD-TIME-VIOLATED" in codes(found), True)

# A past-due PO cannot arrive in the past, however old its due date is.
stale = PurchaseOrder(po="P-2", part="A", qty=10,
                      order_date=date(2026, 8, 20), due_date=date(2026, 8, 30))
check("past due arrives no earlier than today", stale.expected_arrival(10, ASOF), ASOF)
check("past due is not a lead-time violation", stale.slip_days(10), 0)

# --- 2. Box quantity: whole boxes are believed, the open box is not.
p = Part("B", lead_time_days=14, box_qty=5000, on_hand=4800)
check("trusted on hand discounts the open box", p.trusted_on_hand, 0)
check("open box quantity", p.open_box_qty, 4800)
check("no box quantity means take it at face value",
      Part("C", on_hand=4800).trusted_on_hand, 4800)
check("round up to whole boxes", round_to_box(4200, 5000), 5000)
check("exact multiples are not rounded up", round_to_box(10000, 5000), 10000)

# Josh's case: reads as covered, and is only covered by an uncounted open box.
_, found = run(p, [], [DemandLine("B", 4200, date(2026, 10, 19), ref="WO-1")])
check("hidden shortage is found", "PARTIAL-BOX-RISK" in codes(found), True)
check("hidden shortage is critical",
      [f.severity for f in found if f.code == "PARTIAL-BOX-RISK"], ["critical"])
# The same part with the full box on hand is genuinely fine and must stay quiet.
_, found = run(Part("B", lead_time_days=14, box_qty=5000, on_hand=5000),
               [], [DemandLine("B", 4200, date(2026, 10, 19))])
check("a full box raises nothing", codes(found), set())

# --- 3. Coverage: the hole, and whether ordering today can still close it.
part = Part("D", lead_time_days=21, box_qty=500, on_hand=1200)
proj = project(part.on_hand, part,
               [(date(2026, 9, 25), 2000)],
               [(date(2026, 9, 24), 1800)])
check("shortage date", proj.shortage_date, date(2026, 9, 24))
check("shortage quantity", proj.shortage_qty, 600)
check("order-by is the shortage date less lead time",
      order_by(proj.shortage_date, 21), date(2026, 9, 3))

# A receipt landing the same day as the requirement does not cover it.
same_day = project(0, Part("E"), [(date(2026, 10, 1), 100)], [(date(2026, 10, 1), 100)])
check("same-day receipt does not cover the requirement",
      same_day.shortage_date, date(2026, 10, 1))

# Safety stock is a floor, not a cushion to eat into.
floor = project(100, Part("F", safety_stock=50), [], [(date(2026, 10, 1), 60)])
check("dipping below safety stock is a shortage", floor.shortage_date, date(2026, 10, 1))

# --- 4. Parsing, because ERP exports are not tidy.
check("US dates", parse_date("9/24/2026"), date(2026, 9, 24))
check("ISO dates", parse_date("2026-09-24"), date(2026, 9, 24))
check("blank dates", parse_date(""), None)
check("unparseable dates do not raise", parse_date("next Tuesday"), None)
check("thousands separators", parse_num("1,200"), 1200.0)
check("parenthesised negatives", parse_num("(50)"), -50.0)
check("blank quantities", parse_num(""), None)

# --- 5. End to end on the sample data, including the exit code.
result = subprocess.run(
    [sys.executable, "lead_time_review.py", "--data", "sample-data", "--asof", "2026-09-16"],
    cwd=HERE, capture_output=True, text=True)
check("critical findings exit non-zero", result.returncode, 1)
for expected in ("## Act today", "Every part, and where it stands", "What was checked"):
    check(f"packet contains {expected!r}", expected in result.stdout, True)
check("a part with orders but no item master record is reported",
      "UNKNOWN-PART" in result.stdout or "not in the item master" in result.stdout, True)

if FAILURES:
    print(f"{len(FAILURES)} failed:")
    for line in FAILURES:
        print(f"  - {line}")
    raise SystemExit(1)
print("all checks passed")
