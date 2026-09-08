# Episode 002 — captions, rewritten from the recording

One line per cue in `Video Project 3.srt`, **in order, same count**. Clipchamp's
auto-captions are verbatim, so they carry every "So" and every restart; these are the
same beats said tightly. A line of `-` means "no caption here" — that segment is treated
as dead air and compressed.

Deliberate departures from what was said out loud:

- Cue 3 says "N5 through N10"; the dialog on screen shows `=$M$5:$M$10`. **The caption
  says M**, because matching the screen beats matching the audio (style-guide Rule 0).
- Cue 14's point about an unformatted cell at row 11 is dropped. It is a cosmetic wart in
  the workbook, not the lesson, and naming it invites people to look at it.
- Cue 17 is the single word "So" — a caption artifact, not a beat.
- Cue 21 ("Without any rule sets") is cut with `x`, per Josh 2026-09-08: the recap
  card should land immediately after the "next week" line rather than after a
  trailing fragment.

---

Last week's drop-down used Data Validation — with a hard-coded source.
Instead of hard-coding it, point Source at a list of cells.
Select M5 through M10.
Every cost center, in the drop-down.
But that list was typed by hand. Add a cost center and it goes stale.
So make it a formula.
SORT, UNIQUE, the table, and the column we want.
A spill error — not enough empty cells below.
Clear those out.
The list builds itself, sorted alphabetically.
Now add a row to the export, with a new cost center —
Powder Line 2.
Fill in the rest of the line.
Back on the report, the live list grew to seven.
But the drop-down still doesn't have it.
We could edit Data Validation every time. That's the manual work again.
-
So point Source at the array instead: M5, hash. Now it pulls every value, always.
>That's it for this week.
>Next week: Search Folders in Outlook — a folder that fills itself.
x
