# 005 — XLOOKUP, and why you can delete VLOOKUP

**Promised on screen.** 004's recap card ends "Next up: VLOOKUP and XLOOKUP", so this one
is committed before it is written. Excel, after two Outlook episodes — the rotate-apps rule
resumes here.

## The one idea

Not "here is a new function". The idea is: **VLOOKUP can be wrong without telling you**, and
the thing that replaces it removes the whole class of mistake.

Everyone who has used Excel for a year knows VLOOKUP works. Almost nobody has watched one go
quietly wrong. That is the ninety seconds worth spending.

## Why this is the right shape for two minutes

Four differences, but they are not four tips — they are one story told once:

| VLOOKUP | XLOOKUP |
| --- | --- |
| Counts columns, so inserting one **silently returns the wrong column** | Points at a range; an inserted column moves with it |
| Cannot look to the **left** of the key | Lookup and return are separate arguments, so direction is irrelevant |
| Defaults to **approximate** match — you have to remember `FALSE` | Defaults to exact |
| Returns `#N/A`, so you wrap it in `IFNA` | Takes an "if not found" argument |

**The spine is the silent one.** Lead with it, land it hard, and the other three land as
consequences rather than as a feature list.

## The demo, in order

Built by `build_demo_workbook.py` — a fabricated job-cost export, fixed seed, no real
customer, vendor or employee data. Same approach as 001 and 002.

1. **A VLOOKUP that works.** Look a job number up in the export, return its amount. It is
   right. Everyone nods.
2. **Break it without touching it.** Insert a column in the export — the thing anyone might
   do in a week. The formula still calculates, shows **no error**, and returns a number from
   the wrong column. *This is the whole episode.* Hold on it.
3. **Rewrite it as XLOOKUP.** Same answer, and inserting a column does not move it.
4. **Now look left.** Given a part number, return the job number that sits to its left.
   VLOOKUP cannot do this at all — it is not harder, it is impossible.
5. **The missing one.** Look up a job that is not there. `#N/A` versus
   `"Not found"` as the fourth argument, no `IFNA` wrapper.

## What to leave out, deliberately

- **INDEX/MATCH.** It is the correct old answer and it will tempt me into a comparison of
  three things instead of two. One line at most, or nothing.
- **Wildcard and binary search modes** (arguments 5 and 6). Real, and irrelevant to the
  ninety percent.
- **Spilled XLOOKUP returning a whole row.** A genuinely good trick, and a different episode.
- **"VLOOKUP is bad."** It is not; it is fine until someone edits the sheet. The episode is
  about a failure mode, not a scolding — and half the audience has VLOOKUPs they cannot
  rewrite today.

## Version check — do this before recording

**XLOOKUP needs Microsoft 365 or Office 2021.** On Office 2019 and earlier the formula does
not exist, and the episode is useless to anyone still on it. Confirm what the company
actually runs before recording, not after: if a meaningful number of people are on 2019,
the episode needs a fifteen-second "if you don't have it, here's INDEX/MATCH" tail, which
changes the script.

→ **Open question for Josh. See OPEN-DECISIONS.**

## Recording

Excel, not Outlook, so the 003/004 browser rig does not apply directly — but the capture
half does. `capture_window.ps1` grabs any window by title with `PrintWindow`, so it works on
Excel unchanged; only the driving changes, and Excel drives from COM.

Standing rules that already cost a re-record once:

- **Zoom 130–150%.** 100% at 1080p produced the ~11px text that got 002 reported as blurry.
- **Ribbon collapsed** (`Ctrl+F1`) — the tip is not about a ribbon control.
- **Light mode.**
- **Demo workbook only.** Never a live file, and keep the Answer Key sheet off screen.
- **Read every finished frame** before anyone else does.

## Shot list — draft, times to be set by the render

| Say | On screen |
| --- | --- |
| "Welcome to Two-Minute Training." | The export, then the small report beside it |
| "This is a lookup that works. Job number in, amount out." | The working VLOOKUP |
| "Now watch what happens when somebody adds a column." | Right-click, Insert |
| "No error. Just a different number." | **Hold.** The wrong answer, sitting there |
| "It counted to five. Five moved." | The `5` in the formula |
| "Here's the same thing with XLOOKUP." | Type it |
| "No counting. You point at the column you want." | The two ranges |
| "Insert another column. It follows." | Insert again, answer holds |
| "And it looks left, which VLOOKUP simply cannot do." | Part number in, job number out |
| "One more. A job that isn't in the export." | `#N/A` |
| "XLOOKUP will say so in English." | The fourth argument |
| **Over the recap card:** "That's it for this week." | Recap |
| **Over the recap card:** "Next up: <006>." | Recap |

## The outro — needs deciding before recording

004 shipped an outro nobody had agreed and it cost a re-render; 003 did the same. So:
**006 is Athena Lakis's "get rid of the blank rows"**, requested 2026-09-01 and now passed
over twice. The backlog's own rule is that a requested tip beats a chosen one.

→ **Confirm with Josh, and reply to Athena either way** — being visibly answered is most of
the value of taking requests.

## If it runs long, cut in this order

1. The "if not found" argument. Useful, and the least surprising of the four.
2. Looking left. Painful to lose, but the silent-wrong-column point survives without it.

**Never cut** the inserted column. Without it this is a feature tour, and feature tours do
not change what anyone does on Monday.
