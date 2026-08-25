# Episode 002 — Data Validation, the basic way and the way that maintains itself

| | |
| --- | --- |
| **Episode** | 002 |
| **App** | Excel |
| **Tip** | **Data Validation** — a list from a range, then a list from an array formula |
| **Target runtime** | 1:55 |
| **Demo file** | `../001-excel-dynamic-arrays/demo-workbook-solved.xlsx` — generated, see setup |
| **Recap card lines** | 1. `Data → Data Validation → Allow: List` · 2. Basic source: `=$M$5:$M$10` · 3. Live source: `=$O$5#` |

## This one is being SCREEN-RECORDED, not rendered

Josh, 2026-08-25: the synthetic render "isn't showing everything I want", so 002 is recorded for
real from the Excel UI, following [`../../production/recording-sop.md`](../../production/recording-sop.md).

What that changes:

- **`render/` is parked, not deleted.** `TMTT-002-Data-Validation.mp4` and its voiced cut in this
  folder are the synthetic attempt. They are NOT the deliverable and must not be uploaded. The
  renderer stays because a later episode may want it and because it holds the fixed card block.
- **The Say column is now narration to speak, not a caption track.** The synthetic pipeline
  (`make_narration.py`, `make_voiceover.py`) generated audio from captions; a real recording gets a
  real voice, so the timings below are a guide rather than the record.
- **The demo file still applies**, and is still generated rather than hand-built:
  `python ../001-excel-dynamic-arrays/build_demo_workbook.py --solved`.

Everything below — the structure, the runtime warning, the setup checklist, the proof steps — holds
for a real recording unchanged. That was the point of writing it as a shot list.

## The pain, in one sentence

> The drop-down on your report was typed in by hand, so the day somebody adds a
> cost center, the drop-down quietly stops telling the truth.

## Structure: basic, then break it, then fix it

This episode teaches Data Validation twice, and the middle beat is the one that
matters:

1. **Basic** — Allow: List, Source: a range you selected. This is what most of
   the drop-downs in this building are, and it is worth teaching plainly because
   plenty of people have never opened the dialog at all.
2. **Break it** — add a cost center to the export, come back, and the drop-down
   has not changed. No error, no warning. It is simply wrong now.
3. **Advanced** — repoint Source at an array formula's spill range, `=$O$5#`, and
   the same drop-down maintains itself.

Teaching the basic version first is not padding. Without it the `#` looks like
trivia; with it, the viewer has just watched the ordinary approach fail, so the
fix lands as a fix rather than a flourish.

## A runtime warning worth reading before you record

**1:55 against the 2:00 ceiling.** This is the tightest episode in the series so
far and it carries two teaching sections instead of one. Rehearse it once with a
stopwatch before recording anything.

If rehearsal comes in over 2:00, cut in this order:

1. The second drop-down pick at 1:44 — pick once, not twice.
2. The basic version's drop-down-open at 0:30 — you can say it instead of showing
   it.
3. Two words out of every Say line. Tightening beats amputating.

**Do not cut the break-it beat at 0:38–1:05 to buy time.** Without it this is two
disconnected tips and the episode has no argument.

## Setup before recording

This episode opens on last week's finished report, so the demo file is 001's
workbook already solved. Generate it — do not hand-build it:

```
cd ../001-excel-dynamic-arrays
python build_demo_workbook.py --solved
```

That emits `demo-workbook-solved.xlsx` with exactly the state this script needs:
001's three formulas in `B5`/`D5`/`F7`, the six cost centers typed as plain text
into `M5:M10` under a `Cost centers (typed)` label, column `O` clear for the array
formula, and **`G4` still carrying its hard-coded validation list** — that stale
list is the episode's subject, so it is left broken on purpose.

Then check before rolling:

- [ ] Open it once and let Excel calculate — the three spill ranges must be
      showing, not `#NAME?` (which means you are not on Microsoft 365)
- [ ] On the **Report** sheet, `G4` reading `Powder Line 1`
- [ ] The typed `M5:M10` list is in **entry order, not alphabetical** — that is
      deliberate. When the array formula sorts it at 1:20, the difference is
      visible on screen and sells the point for free.
- [ ] **Answer Key** sheet present but not clicked on camera
- [ ] Display 1920×1080, Excel zoom 140%, ribbon **expanded** — this episode lives
      in the Data tab, so the ribbon has to be visible. The one episode that
      breaks the collapsed-ribbon habit.
- [ ] Do not disturb on, Teams on DND, Outlook closed

## Script

Read the **Say** column out loud. The **Do** column is your hands. Times are
where each beat *starts*.

| Time | Say | Do |
| --- | --- | --- |
| 0:00 | "Welcome to Two-Minute Training Tuesday." | Title card, 3.7 s |
| 0:04 | "Last week this drop-down changed the whole report. Here's what I didn't tell you — I typed those six names in by hand." | On **Report**. Click **G4**, open the drop-down, close it. |
| 0:12 | "The feature behind every drop-down in Excel is called Data Validation. Here's the basic way to build one." | Click **G4**. **Data** tab → pause on **Data Validation** so the button is seen → click it. |
| 0:20 | "Allow: List. And for Source, just select the cells your list lives in." | **Allow** → **List**. Click into **Source**, clear it, then drag-select **M5:M10** on the sheet. |
| 0:30 | "OK. That's a working drop-down, and it's how most of ours are built." | **OK.** Open the **G4** drop-down. Six names. Close it. |
| 0:38 | "Now watch it fail." | Click the **ERP Export** tab. |
| 0:42 | "New line on the export. New cost center — Powder Line 3." | On the first empty row under the table, type a date, a job number, and **Powder Line 3**. Type it, do not paste it. |
| 0:52 | "Back to the report. Open the drop-down." | Click the **Report** tab. Open the **G4** drop-down. |
| 0:57 | "Still six. The export knows about Powder Line 3. The drop-down doesn't, and it will never tell you." | Hold on the open drop-down a full second. Close it. |
| 1:05 | "So point Source at a formula instead of at cells I typed." | Click **O5**. |
| 1:10 | "SORT and UNIQUE from last week, on the cost center column." | Type `=SORT(UNIQUE(` then click the **ERP Export** tab and the **Cost Center** column header. Close both parens. |
| 1:20 | "Enter. Seven — it read the data, including the row I just added." | **Enter.** Let it spill. Pause. |
| 1:27 | "Same dialog. New Source." | Click **G4**. **Data** → **Data Validation**. Click into **Source** and clear it. |
| 1:34 | "O5, hash. The hash means this cell and everything the formula spilled into — however many that turns out to be." | Type `=$O$5#`. Pause so it is readable. **OK.** |
| 1:44 | "There it is. Powder Line 3, and I never touched the drop-down." | Open the **G4** drop-down — seven names. Pick **Powder Line 3**. Let the report redraw. |
| 1:52 | "Next week: Outlook. Find any attachment in four seconds." | Recap card, 4 s |

## Proof step

**Two proofs, and together they are the spine of the episode.**

The first is the *failure* at 0:57 — the basic drop-down still showing six after
the export gained a seventh. Hold on it. A viewer who does not feel that beat has
no reason to care about the second half.

The second is 1:44 — the same drop-down, now seven, with no edit in between. Pick
**Powder Line 3** and let the FILTER report redraw underneath it, which quietly
reuses everything from episode 001.

Type the new export row on camera rather than pasting it. Watching something
ordinary get typed is what makes the update feel real rather than staged.

## Recap card

```
Data → Data Validation → Allow: List
Basic source:  =$M$5:$M$10
Live source:   =$O$5#
```

## Written summary for the post

> Every drop-down in Excel is the **Data Validation** feature, and there are two
> ways to feed it. The basic way: select the cell, then **Data → Data Validation
> → Allow: List**, and set **Source** by selecting the range your list sits in,
> like `=$M$5:$M$10`. That works, and it is how most of our spreadsheets are
> built — but it goes stale silently the moment someone adds a cost center,
> because the range you selected does not grow.
>
> The better way points Source at an array formula instead. Put
> `=SORT(UNIQUE(ERP_Export[Cost Center]))` in a cell — say `O5` — and set
> **Source** to `=$O$5#`. That `#` is a *spill reference*: it means "this cell and
> every cell this formula filled." The list now grows and shrinks with the data on
> its own, so a new cost center in the export shows up in the drop-down with no
> edit. You can hide the helper column; the reference still works.
>
> Needs Microsoft 365. Use the dollar signs — a relative reference gives you an
> empty drop-down and no error message.

## Gotchas to mention (or deliberately skip)

- **Say this on camera:** needs **Microsoft 365**. The basic range version works
  in any Excel; the `#` in a Data Validation source is the part older versions
  choke on.
- **Absolute reference matters.** `=$O$5#`, not `=K5#`. Data Validation stores the
  source relative to the selected cell, so a relative reference silently points
  somewhere else when the rule is copied. Four seconds well spent — the failure is
  an empty drop-down with no error.
- **Why not a Table column for the basic version?** Because a structured
  reference in a Data Validation Source is unreliable across versions — which is
  part of why the spill reference is the better answer. **Skip on camera** unless
  someone asks; it is a whole second idea.
- **If the helper list lives on another sheet**, name the range and point Source
  at the name. Cross-sheet spill references in Data Validation are unreliable.
  Comments only.
- **Skip on camera:** `ANCHORARRAY`, the `@` operator, and Excel's own
  "extend the range?" prompts. All true, none of it fits in two minutes.

## Next-episode hook

> "Next week: Outlook. Find any attachment in four seconds, without scrolling."
