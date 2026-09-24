# `Training Samples` — contents, and why the Cc demo is not possible

Read from the mailbox 2026-09-24. **Josh picked these**, after my first proposal (twelve
Two-Minute Training messages, nine from Josh) turned out to be safe but useless as a demo: a
list of near-identical subjects from one sender is not an inbox, and coloring it shows nothing.

| # | From | Subject | Date |
| --- | --- | --- | --- |
| 1 | Thomas Feddeler | Re: HW Period 9 Week 5 OPEX Reports | 09-22 |
| 2 | Scott Bruick | Organizational Announcement! | 09-21 |
| 3 | Jennifer Wilson | RE: MP Period 09 Week 4 OPEX Report | 09-21 |
| 4 | Stephen Geist | FW: [External] Purchase Order 4500776697 | 09-21 |
| 5 | Angela Stuckey | RE: [External] S56-1070/R Door Handle … Inteva to PACCAR RESCHEDULE | 09-08 |
| 6 | Abraham Norton | Re: MP Finance meeting | 08-20 |

Preview text is off, so only sender and subject render. Six rows fill the list without
scrolling.

## `I'm not on the To line` colors NOTHING here — tested live, 2026-09-24

**This settles a question that got answered wrong twice, in both directions.** It was first
asserted (correctly, but by guesswork) that the rule would color nothing; then "corrected" to
say two of six would fade, on the strength of reading each message's To and Cc fields; that
correction is what this file used to say. Neither was a test. This is.

A real rule was built in the live mailbox — `Copied in`, one condition, `Font color` → Silver,
sitting **first** in the order — and its condition swapped three times, with a full settings
reload between each so the client re-hydrated:

| Condition | What actually colored |
| --- | --- |
| `I'm on the To or Cc line` | **Everything.** All six here and the whole Inbox went silver, overriding Cranberry on Geist and Norton — so the rule, the color and the ordering all work. |
| `I'm on the Cc line` | **Nothing.** |
| `I'm not on the To line` | **Nothing.** |

The first row is the control, and it is what makes the other two conclusive: the mechanism is
not broken, the condition family is not ignored on existing mail, and a first-position rule
does win. The answer is simply that **Josh is on the To line of all six messages**, including
Scott Bruick's `Organizational Announcement!`, which is addressed to a distribution list —
Outlook resolves that as being on the To line, not as "not on the To line".

**Consequence for the episode:** the copied-in rule can be *named* but not *demonstrated* with
this folder, which is exactly what the shipped 1:15 cut does. Do not re-open this without new
messages: the fix is not a different rule, it is a message in the folder that Josh is genuinely
only copied on.

**Nothing was left behind.** The `Copied in` rule was deleted, `Finance` was re-enabled, and the
Inbox was re-checked rendering Cranberry and Light green exactly as before.

## One subject worth a second look

**#5** names two customers (Inteva, PACCAR), a part number and RESCHEDULE. Raised with Josh
2026-09-22; he picked the set and did not swap it. Noted, not re-litigated.
