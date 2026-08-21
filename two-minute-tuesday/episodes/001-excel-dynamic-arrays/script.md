# Episode 001 — Stop copy-pasting your vendor list

| | |
| --- | --- |
| **Episode** | 001 |
| **App** | Excel |
| **Tip** | `UNIQUE`, `SORT`, `FILTER` |
| **Target runtime** | 1:49 |
| **Demo file** | `demo-workbook.xlsx` (380 rows, 15 vendors, 6 cost centers) |
| **Recap card lines** | 1. `=UNIQUE(range)` · 2. `=SORT(UNIQUE(range))` · 3. `=FILTER(table, column = criteria)` |

## The pain, in one sentence

> Every month you copy the vendor column into a new tab, run Remove Duplicates,
> sort it, and then do the whole thing again next month because the export
> changed.

## A scope warning worth reading before you record

Three functions in under two minutes is genuinely tight — about 30 seconds each.
It is doable, and it is also exactly the kind of thing the two-minute format
exists to stop. Record it as one episode as written. **If your rehearsal comes in
over 2:00, cut the `FILTER` section entirely**, end after `SORT`, and publish
`FILTER` as episode 002 (it is already sitting in the backlog for that reason).
Two clean Tuesdays beat one rushed one.

## Setup before recording

- [ ] `demo-workbook.xlsx` open, on the **ERP Export** sheet, scrolled to the top
- [ ] **Answer Key** sheet — check your formulas against it, then leave it. Do not
      delete it; just do not click it on camera.
- [ ] **Report** sheet confirmed blank apart from its labels, and `G4` reading
      `Powder Line 1`
- [ ] Display 1920×1080, Excel zoom 140%, ribbon collapsed (Ctrl+F1), formula bar
      **visible** — it is the star of this episode
- [ ] Do not disturb on, Teams on DND, Outlook closed
- [ ] Mic verified with a 5-second test take

## Script

Read the **Say** column out loud. The **Do** column is your hands. Times are
where each beat *starts*.

| Time | Say | Do |
| --- | --- | --- |
| 0:00 | *(silent)* | Title card, 2.5 s |
| 0:03 | "This is a job cost export out of the ERP. Three hundred and eighty lines, and it lands in your inbox every month." | On **ERP Export**. Scroll down a few pages at a readable speed, then Ctrl+Home back to the top. |
| 0:09 | "You need the list of vendors we actually bought from. So today you copy this column, paste it into a new tab, Remove Duplicates, sort it — and next month you do all of it again." | Click the **Vendor** header, drag-select a chunk of the column so it is clear which column you mean. |
| 0:18 | "Here's the version that never needs doing twice." | Click the **Report** tab. |
| 0:22 | "One formula. UNIQUE — U, N, I, Q, U, E — and the vendor column." | Click **B5**. Type `=UNIQUE(` then click the **ERP Export** tab and click the **Vendor** column header so Excel writes the structured reference for you. Close the paren. |
| 0:32 | "Enter." | **Enter.** Let the list spill down. Pause a full second — this is the moment. |
| 0:35 | "Fifteen vendors, out of three hundred and eighty lines, from one formula. I never told it fifteen. It figured that out and it took the space it needed." | Move the mouse down the spilled list. Click one cell mid-list and point at the greyed-out formula in the formula bar. |
| 0:44 | "Every cell in that list belongs to the one formula in B5. That's called a spill range, and the blue border is Excel telling you so." | Click **B5** so the spill border shows. |
| 0:52 | "It's not sorted, though. So wrap it in SORT." | Click **D5**. Type `=SORT(UNIQUE(` and reference the same Vendor column, close both parens. |
| 1:00 | "Enter. Alphabetical, and still one formula." | **Enter.** Pause. |
| 1:05 | "Now the useful one. FILTER. Give it the whole table, then tell it which rows you want." | Click **F7**. Type `=FILTER(` |
| 1:12 | "The table..." | Click the **ERP Export** tab, click cell **A2**, and press **Ctrl+A** to grab the whole table — or type `ERP_Export`. Type a comma. |
| 1:18 | "...and the rule: cost center equals whatever's in this cell." | Reference the **Cost Center** column, type `=`, click back to **Report** and click **G4**. Close the paren. |
| 1:26 | "Enter." | **Enter.** A hundred and thirty-six rows spill out across six columns. Pause a beat and let the size of it land. |
| 1:30 | "Every line charged to Powder Line 1. And here's the part that matters —" | Hover **G4**. |
| 1:34 | "— change the cost center, and the whole report redraws itself." | Click **G4**, open the dropdown, pick **Shipping**. Pause. Then pick **Prep & Blast**. Pause. |
| 1:42 | "No copying. No pasting. No re-sorting. Next Tuesday." | — |
| 1:45 | *(silent)* | Recap card, 4 s |

## Proof step

The dropdown change at 1:34 is the proof, and it is the whole episode. Do not
rush it and do not talk over it. Click, pause, let the viewer watch 136 rows
become 62. **If you cut anything for time, do not cut this.**

Stronger proof if you have the seconds to spare: go to the **ERP Export** sheet,
type a brand-new vendor name on the first empty row below the table, come back,
and show it already present in the sorted list. The table auto-expands, so the
formulas pick it up with no edit at all.

## Recap card

```
=UNIQUE(range)
=SORT(UNIQUE(range))
=FILTER(table, column = criteria)
```

## Optional cold open (worth the two minutes of editing)

Retention on internal video is won or lost in the first ten seconds. In
Clipchamp, copy the 1:34–1:42 dropdown segment, paste it at the very front right
after the title card, and trim it to about 4 seconds. Viewers see the payoff
before they are asked to invest in the explanation. Trim an equivalent 4 seconds
out of the 0:09 pain beat so the runtime holds.

## Written summary for the post

> Three Excel functions replace the copy-paste-dedupe-sort routine on any export.
> `=UNIQUE(range)` returns the distinct values in a column. Wrap it in `SORT` —
> `=SORT(UNIQUE(range))` — to get it alphabetical. And
> `=FILTER(table, column = criteria)` returns every row matching a condition,
> where the condition can point at a cell, so changing that one cell redraws the
> whole report. All three write their own results into as many cells as they need
> — that is a "spill range" — so you never drag a formula down again. The demo
> workbook is attached if you want to try it on the real thing.

## Gotchas to mention (or deliberately skip)

- **Say this on camera:** these need **Microsoft 365 or Excel 2021**. On Excel
  2019 or 2016 the functions do not exist and you will get `#NAME?`. Better to
  say it in five seconds than to field ten messages about it.
- **`#SPILL!`** means something is already sitting in the cells the formula wants
  to fill. Clear them and it resolves itself. Mention only if it happens live —
  and if it does, keep going and fix it on camera. It is the most common error
  people will hit, so watching you fix it calmly is useful.
- **Skip on camera:** the `@` implicit-intersection operator, and the difference
  between `ERP_Export` and `ERP_Export[#All]`. Both are correct, neither belongs
  in a two-minute video.

## Next-episode hook

> "Next Tuesday: that spilled list has an address — `B5#` — and it makes
> drop-downs that maintain themselves."
