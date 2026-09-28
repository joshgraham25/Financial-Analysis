# Episode 005 — lines to read

**Excel, M365** (confirmed 2026-09-28 — everyone is on M365, so XLOOKUP is safe to use and
there is no INDEX/MATCH fallback beat).

Demo workbook: `build_demo_workbook.py` → `demo-workbook.xlsx`, fixed seed. The numbers below
are that seed's, so **re-check them if the workbook is ever regenerated with a different one**:

- Lookup job `J-4277`, whose real Amount is **1,228.18**
- Its Cost Center is **2100** — what the broken VLOOKUP returns
- Part `MNT-532` is on that same job, so the look-left demo agrees with the first demo
- `J-9999` is not in the export

**The outro names 006, which is not confirmed yet** — see OPEN-DECISIONS item 8. Do not
render until it is; 003 and 004 both cost a re-render for exactly this.

---

Welcome to Two-Minute Training.
This is a job cost export, and a little report that looks one job up in it.
The formula is a VLOOKUP. Job number in, amount out.
Twelve twenty-eight. That's right, and it's been right for months.
Now somebody adds a column to the export.
Not to the formula. To the sheet. The thing anyone might do in a week.
Look at the answer.
Twenty-one hundred.
No error. No warning. Just a different number that looks exactly like a dollar amount.
That's a cost center. The formula is reading the wrong column.
Because VLOOKUP counts. I told it five, and five moved.
Here's the same lookup, written as XLOOKUP.
Nothing to count. You point at the column you're searching, and the column you want back.
Add another column. The answer doesn't move.
There's a second thing it fixes.
VLOOKUP can only look to the right of what you search.
So if I have a part number and I want the job it's on, VLOOKUP can't. Not harder. Can't.
XLOOKUP doesn't care which side it's on.
And one last one. A job that isn't in the export.
VLOOKUP gives you N/A, and you wrap it in something to hide it.
XLOOKUP just lets you say what to show instead.
Not found. In English, where anyone can read it.
So: no counting, either direction, and it tells you when it finds nothing.
That's it for this week.
