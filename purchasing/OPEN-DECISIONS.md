# Open decisions — purchasing review

Same convention as the series file: answer on the `→` line, leave the question in place. I
read this at the start of a session, so an answer here needs no chat round trip and survives
the session ending.

The engine and the packet are built and tested against sample data. Everything below is about
pointing them at the real numbers — none of it blocks reading
[`reviews/2026-09-16.md`](reviews/2026-09-16.md) to see whether the checks are the right
checks.

---

## Open

### 1. Which system, and can the three exports come out on a schedule? `Blocked`

The review reads `parts.csv`, `open_pos.csv`, `demand.csv` from a folder, with column names
mapped in `source-map.json`. That is deliberate — it works with a hand-run export out of
anything, and adapting to a new export is an edit to one JSON file.

What it cannot do yet is get the files by itself. Two ways forward, and the answer decides
which:

1. **Somebody exports three files Monday morning** and runs one command. Works this week,
   costs five minutes a week, and rots the first Monday somebody is out.
2. **A scheduled pull** — ODBC/SQL against the ERP, or a saved export dropped on a share.
   Then the packet is waiting when the meeting starts, and the ledger at the top catches it
   when a feed goes stale.

(2) is where this should end up, and it needs the system name and read access to know what it
costs. **Start with (1) this week regardless** — the checks are worth running by hand, and
running them by hand is how we find out whether the columns mean what we think they mean.

→ *(open — needs the ERP name, and whether read access is gettable)*

### 2. Calendar days or working days for lead time? `Decision`

The code treats `lead_time_days` as **calendar days** throughout — `order_date + lead_time`
and `shortage_date − lead_time` both count weekends.

This matters more than it sounds. On a 21-day lead time the two readings are about nine days
apart, and nine days is the difference between *order this week* and *already late*. If the
item master holds working days, every order-by date in the packet is optimistic — which is
the wrong direction to be wrong in.

→ *(open — if it is working days, say so and it becomes a one-line change plus a re-run)*

### 3. What counts as demand? `Decision`

`demand.csv` is currently "every dated requirement". Josh's words were *current demand at
full*, which I have read as: do not net anything out before it gets here.

The specific question is what goes in the file:

- Released work orders — yes, obviously.
- Firm sales orders not yet released to a work order — **probably yes**, they are real
  material with a date.
- Blanket releases and forecast — **probably not**, or they will drown the packet in
  shortages that never happen.

Getting this wrong in the generous direction is the safer failure: an over-full packet is
annoying, an under-full one is the thing we are trying to stop. But it is worth one decision
rather than discovering it in the meeting.

→ *(open)*

### 4. Is there a box-quantity field, and is it the right one? `Blocked`

The partial-box check is only as good as this number. Most systems carry two or three that
look alike — purchase multiple, order multiple, minimum order quantity, standard pack. The
one this needs is **the physical quantity in a sealed box**, because the whole logic is *a
sealed box can be counted at a glance and an open one cannot*.

If the field that exists is really a minimum order quantity, the check still runs and means
something different, and the packet will say confident things about boxes that are not boxes.

→ *(open — needs somebody to look at what is actually in the field, on a handful of parts)*

### 5. Is safety stock maintained, and is it a floor? `Decision`

Safety stock is optional in the input and treated as a **floor** — dipping into it is a
shortage. If the field is maintained but stale, or is used as a reorder point rather than a
floor, the packet will report shortages that are not shortages, and people stop reading it by
week three. Leaving the column out entirely is a fine answer.

→ *(open)*

### 6. Who owns the meeting? `Decision`

`weekly-review-sop.md` describes a thirty-minute Monday sit-down. It needs a name against it
and a standing invite, or it becomes the email it was meant to replace.

→ *(open)*

---

## Settled

### The review projects every part twice, and the sceptical number is not a warning

Whole boxes are believed, the open box is discounted entirely. A part sitting below one full
box is treated as **zero** until somebody counts it. This is deliberately harsher than the
system number, because the open box is the one quantity nobody has ever verified, and the
failure it causes lands at the machine rather than in a report.

Where a part is already being reported short, the open box appears inside that finding as a
bigger number rather than as a second finding — one part, one row of work.

### Expected arrival believes lead time over the due date

An open PO's arrival is the latest of: its due date, `order_date + lead_time`, and today. A
past-due PO cannot arrive in the past, and a due date inside the lead time is not a date, it
is a wish.

### A part with missing data is reported, not skipped

No lead time, no box quantity, no order date on a PO, undated demand, negative on hand, a
part number not in the item master — each is a finding in its own section. A part missing its
lead time passes every other check *by default*, and that silence is the failure mode the
whole review exists to break.

### The packet leads with what it looked at

Counts of parts, lead times, PO lines, order dates and demand lines, before any finding. It
is what lets the meeting honestly say *I looked at every one*, and it is what catches a feed
that quietly stopped — a drop in the counts is a bigger problem than anything below it.
