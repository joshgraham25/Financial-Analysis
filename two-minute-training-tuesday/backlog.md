# Episode backlog

Ordered roughly by *how much time it saves × how many people it affects*, not by
how clever the trick is. Pull from the top; when a request comes in from a
comment, it jumps the queue — a tip somebody asked for beats a tip you chose.

Rotate apps week to week. Four Excel episodes in a row and the people who don't
live in Excel stop watching.

## Rules for adding to this list

- One tip per line. If it needs "and", it is two episodes.
- It must be demonstrable in under 100 seconds of screen time.
- It must be demonstrable without real customer or employee data on screen.
- Prefer the thing people do wrong *weekly* over the thing they do wrong *once*.

---

## Queued

Struck-through numbers are done. `=$M$5#` in 002 is correct and `=$K$5#` was not: the
helper list moved from J/K to M when it turned out J:K sits inside 001's `F:K` FILTER
spill and threw `#SPILL!`.

| # | App | Working title | The pain it kills |
| --- | --- | --- | --- |
| ~~001~~ | Excel | Stop using copy and pasting to get a unique list | `UNIQUE`, `SORT`, `FILTER` — **published 2026-08-25 and emailed** |
| ~~002~~ | Excel | Data Validation, basic then self-maintaining | Allow: List from a range, watch it go stale, then repoint Source at `=$M$5#` so it maintains itself — **recorded and cut 2026-09-08, awaiting upload** |
| ~~003~~ | Outlook | The Outlook folder that fills itself | **Search Folders** — a saved search that looks like a folder, so mail collects itself instead of being filed by hand. The mail never moves, which is the difference from a rule. **Recorded, cut (1:42) and published to the library 2026-09-25. NOT yet announced.** Ships carrying the old branding -- 'Tuesday', 'Next week', 'colour' -- because its frames were swept before they were committed, so fixing it means re-recording |
| — | Outlook | ~~Find any attachment in four seconds~~ | Folded into 003 as one of the demo criteria ("anything with a big attachment"), rather than its own episode. It is a one-off trick; Search Folders is a habit |
| ~~004~~ | Outlook | **Color-code your inbox without moving anything** | **Josh's idea, 2026-09-17** — Outlook's own *conditional formatting* (`Settings → Mail → Conditional formatting`): a rule that paints matching messages a color in the list instead of filing them. Natural sequel to 003: both make Outlook organize itself without mail ever moving. **Josh chose this as 004 on 2026-09-17**, over Athena's request and ahead of Teams — deliberately two Outlook episodes running, so the rotate-apps rule is waived here, not forgotten. **Recorded, re-cut to 1:59 on 2026-09-25 and published to the library. NOT yet announced.** Two rules built on camera: From -> Cranberry, and I'm-not-on-the-To-line -> Silver |
| 005 | Excel | XLOOKUP, and why you can delete VLOOKUP | Looking left, exact-match default, and the "if not found" argument. **Josh chose this as 005 on 2026-09-21**; 004's outro promises it on screen, so the subject is committed. **Scripted 2026-09-28** with a seeded demo workbook; the spine is a VLOOKUP that returns the WRONG COLUMN with no error after somebody inserts one. **Blocked on a version check: XLOOKUP needs M365 or Office 2021** |
| 006 | Excel | **Get rid of the blank rows** | **Requested by Athena Lakis, 2026-09-01**, replying to 001 — a request beats a tip we chose, per the rules above. Filtering blanks out, or `FILTER` with a not-blank test, instead of sorting and deleting by hand. **Deferred twice already** (at 003 and again at 004) against the rule directly above that a request beats a chosen tip. It should not slip a third time, and Athena is owed a reply either way |
| 007 | Teams | Never lose a message again | Saved messages, plus `Ctrl+E` search with `from:` and `in:` filters |
| 008 | ERP | *(fill in: the one report everybody exports and hand-edits)* | Ask the three heaviest users what they re-key every week |
| 009 | Outlook | Rules that actually reduce your inbox | One rule, one folder, built live — not twelve rules nobody maintains |
| 010 | Excel | Paste values without touching the mouse | `Ctrl+Alt+V` then `V`, plus paste-transpose |
| 011 | Windows | The clipboard remembers the last 25 things | `Win+V` history, and pinning an item you paste all day |
| 012 | Teams | Stop scheduling meetings that could be a channel post | @mentions, replies-in-thread, and marking a post Important |
| 013 | Excel | Flash Fill reads your mind | Splitting names, job numbers, and part codes without a formula |
| 014 | Outlook | Two calendars, one view | Overlay mode and shared calendar permissions |
| 015 | Excel | Freeze the panes, keep your place | Freeze Panes vs. Split, and why the wrong cell selection breaks it |
| 016 | Windows | Snap layouts and virtual desktops | `Win+Z`, `Win+Ctrl+D` — one desktop for the ERP, one for email |
| 017 | Excel | TEXTSPLIT and TEXTJOIN | Turning one messy cell into columns and back |
| 018 | Teams | Record and caption your own walkthrough | So anyone can answer their own "how do I" question — the meta-episode |
| 019 | Outlook | Delay send, and unsend | Deferred delivery and the recall window |
| 020 | Excel | Conditional formatting that flags the exception | One rule on one column: negative margin, past-due, over budget |
| 021 | ERP | *(fill in: the export → Excel handoff everybody does manually)* | |
| 022 | Excel | PivotTables in 90 seconds | Not a tour of PivotTables — one specific question answered with one |
| 023 | Outlook | Quick Steps | The three-click routine you do forty times a day, on one button |
| 024 | Excel | Named ranges make formulas readable | `=Amount * TaxRate` instead of `=F2*$K$1` |
| 025 | Teams | Loop components vs. attachments | When to send a living document instead of `v3_final.xlsx` |
| 026 | Excel | SUMIFS with more than one condition | Cost center *and* month *and* category, without filtering by hand |
| 027 | Windows | PowerToys PowerRename | Renaming 200 files by pattern — *check IT policy on install first* |
| 028 | Excel | Why your numbers won't add up | Text-formatted numbers out of the ERP export, and the three ways to fix them |
| 029 | Outlook | Categories and a search folder | A view of "everything waiting on me" that maintains itself |
| 030 | Excel | Tables, and why every export should be one | Structured references, auto-expand, and formulas that follow new rows |
| 031 | Teams | Channel files are just SharePoint | Sync a channel folder to File Explorer and stop emailing attachments |
| 032 | Excel | Group and outline | Collapsible detail rows on a report someone else has to read |

## Notes on the ERP episodes

Episodes 006 and 019 are deliberately blank. Naming the ERP tip correctly needs
one conversation, not a guess: ask the two or three people who spend the most
hours in it **what they re-type into Excel every week**. That answer is worth
four episodes, and those will be the most-watched ones in the series, because ERP
pain is the pain nobody has ever made a video about.

When you do record them, two extra rules apply:

- Use a **sandbox or test company** if one exists. If not, use test records you
  created yourself.
- Do a dry pass and check **every corner of the frame** for a customer name or a
  dollar figure that should not be published internally.

## Retired / rejected

Keep this section honest — it stops the same bad idea coming back every quarter.

| Idea | Why not |
| --- | --- |
| "Top 10 Excel shortcuts" | Ten tips is zero tips. Nobody remembers a list. One per Tuesday. |
| Macros / VBA intro | Cannot be taught in two minutes, and most of this audience should not be writing macros. |
| Power Query full walkthrough | Genuinely valuable and genuinely a 20-minute topic. Do it as a separate lunch-and-learn, then link the recording from a Tuesday episode. |
| Keyboard shortcut of the week | No outcome in the title, so nobody knows whether to care. A shortcut needs the job it does attached to it. |
