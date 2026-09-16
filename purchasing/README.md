# Purchasing review

Something that looks at every lead time, every open order, every order date, the on-hand
number and the demand behind it — weekly, in one pass, and says so out loud.

## The problem this is against

Purchasing gets fixed one part at a time. The part that screams gets handled, and nobody
goes back for the reason it screamed. Two specific failures keep costing money:

**A PO goes in that violates the supplier's lead time.** Nothing looks wrong. The order sits
there with a due date on it, the schedule is built on that due date, and the first person to
notice is the supplier — on the day it was due, saying *you violated lead time, you will have
it in four weeks*. By then the only options are expensive.

**The box you think holds 1,000 holds 200.** Material that ships in boxes of 5,000 shows a
balance of 1,200. One box you can trust and an open box nobody has counted. The plan rests on
the open box, and the shortfall turns up at the machine.

Both are invisible to a report that only lists exceptions, because in both cases the system
looks fine.

## What it checks

Per part, every week:

| | |
| --- | --- |
| **Lead time vs. order date** | An open PO's real arrival is `order_date + lead_time`, not the due date somebody typed. Where those disagree the due date is fiction, and it is reported now rather than on the due date. |
| **Current on hand** | Taken as given, and also taken sceptically — see box quantity. |
| **Current demand, at full** | Every dated requirement, not net of whatever somebody decided to ignore. |
| **Box quantity** | Whole boxes are believed. The open box is not. Every part is projected twice, and a part that only survives on its open box is a part to go count — not a part that is fine. |
| **The data itself** | Missing lead time, missing box quantity, a PO with no order date, undated demand, negative on hand, a part number that is not in the item master. Each of these makes a part *pass every other check by default*, which is how a part goes quiet. |

For each part it then answers the only question that matters: **when does this go short, and
has the last honest order date already passed?** If it has, ordering today does not fix it —
and entering it as though it does is how the next lead-time violation gets created.

## Running it

```sh
python lead_time_review.py --data sample-data --out reviews/2026-09-21.md
python lead_time_review.py --data ~/exports --asof 2026-09-21 --findings findings.csv
```

Stdlib only, no install. Exit code is 1 when there is anything critical, so it can gate a
scheduled job. `--horizon` (default 7) sets how far ahead an order-by date counts as this
week's work.

`reviews/2026-09-16.md` is a full packet built from `sample-data/`, which exercises every
check. Read it to see the shape before wiring real data in.

Tests: `python test_lead_time_review.py`.

## The input contract

Three CSVs in one folder. Column headers come from `source-map.json`, matched
case-insensitively, so pointing this at a different ERP export is an edit to that file rather
than to the code. Extra columns are ignored.

**`parts.csv`** — one row per purchased part.

| Field | Required | Notes |
| --- | --- | --- |
| `part` | yes | The key everything joins on. |
| `lead_time_days` | effectively | Missing means every lead-time check is skipped and reported as a data gap. |
| `box_qty` | effectively | The purchase multiple — box, case, reel. Missing means partial-box error cannot be seen. |
| `on_hand` | yes | Defaults to 0. |
| `safety_stock` | no | Treated as a floor, not a cushion. Defaults to 0. |
| `description`, `supplier`, `uom` | no | Make the packet readable. |

**`open_pos.csv`** — one row per open PO line. `part`, `qty`, `order_date`, `due_date`;
`po`, `line`, `supplier` optional. **The order date is what makes this work** — without it a
line's due date cannot be checked against anything.

**`demand.csv`** — one row per dated requirement. `part`, `qty`, `need_date`; `source` and
`ref` optional. Undated rows are reported rather than dropped.

Dates parse in the usual formats (`2026-09-24`, `9/24/2026`, `24-Sep-2026`). Quantities
tolerate `1,200`, `$1200.00` and `(50)` for negative.

## What this does not do

It reads exports. It does not connect to the ERP, does not write anything back, and does not
place orders — every action in the packet is for a person. See `OPEN-DECISIONS.md` for what
it would take to pull the exports on a schedule rather than by hand.

It also only knows what is in the three files. A requirement nobody entered is a requirement
this cannot see, which is why the packet leads with a count of what it looked at.
