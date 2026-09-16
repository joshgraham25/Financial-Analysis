# The weekly purchasing review

Josh, 2026-09-16: *"not just an email, but an actual sit-down review."*

An email gets skimmed by people who assume somebody else read it. The point of this being a
meeting is that somebody has to say, out loud, what they are doing about each line — and the
packet exists so that nobody spends the meeting assembling facts.

## Before the meeting

Generate the packet Monday morning, off exports taken that morning:

```sh
python lead_time_review.py --data ~/exports --out reviews/$(date +%F).md
```

Read the top two sections before you walk in. The packet is the agenda, not the minutes.

## The meeting

Thirty minutes, same time weekly, purchasing plus whoever owns the schedule.

**1. Read the ledger out loud.** The *What was checked* table — parts, lead times, open PO
lines, order dates, demand lines. This is the claim the whole exercise rests on: *I looked at
every lead time, every open order, and every order date.* If the counts dropped since last
week, something stopped exporting, and that matters more than any single line below it.

**2. Act today.** Every line gets a name and a date before you move on. Two kinds:

- *Past the last honest order date.* Ordering today does not fix these. The decision is
  expedite, split, or move the job — and **the due date that goes in the system is the one
  the supplier agreed to**, not the one the schedule wants. Entering the wishful date here is
  precisely how next month's violation gets created.
- *Placed inside its own lead time.* Call the supplier now and get a committed date, while
  there is still room to plan around it. The alternative is finding out on the due date.

**3. Order this week.** Order-by dates that will not survive until the next review. These are
cheap now and expensive in seven days. Place them, or decide not to and say why.

**4. Count before you trust it.** Parts that are only covered by an open box. These are
physical-count assignments with a name against them, due before the next review. Nothing on
this list gets ordered off the system number.

**5. Fix the data.** The shortest section and the one that decides how good next week's
review is. A part with no lead time passes every check by default — it is not fine, it is
unexamined. Missing box quantities, POs with no order date, undated demand, negative
balances, part numbers not in the item master. Assign them.

**6. The full table.** Skim, do not read. It is there so the review can prove it covered
everything, and so a part that has been drifting toward trouble is visible before it arrives.

## After

The packet is committed under `reviews/`. Week over week it is the record of what was known
and when — which is the thing that is missing when a part fails and nobody can say whether it
was predictable.

## The one rule

**Never enter a due date the supplier has not agreed to.** Every other problem in the packet
is recoverable. That one manufactures the failure it is meant to prevent, and hides it behind
a system that looks correct until the day it matters.
