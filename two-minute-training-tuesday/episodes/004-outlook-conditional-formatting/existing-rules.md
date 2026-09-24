# Josh's live conditional formatting rules

## CURRENT MAILBOX STATE — 2026-09-24, nothing outstanding

| Rule | State |
| --- | --- |
| `Stephen/Abe` | **Live.** Rebuilt on camera during the 004 capture, identical to the original. |
| `Finance` | **Live and enabled.** Josh renamed it from `John/Thommy/Caleb`. |

Both rules are exactly as Josh had them. Several edits were opened and **discarded** while
exploring the formatting options on 2026-09-24 — none were saved.

## Rule 1 — `Stephen/Abe`

| | |
| --- | --- |
| **Condition** | `From` |
| **People** | `sgeist@creativeliquidcoatings.com` · `AbrahamNorton@creativeliquidcoatings.com` |
| **Formatting** | `Font color` → **Cranberry** |

## Rule 2 — `Finance` (was `John/Thommy/Caleb`)

| | |
| --- | --- |
| **Condition** | `From` |
| **People** | `ThomasFeddeler@…` · `JohnPiebenga@…` · `JenniferWilson@…` **plus "+3 others" that cannot be read** |
| **Formatting** | `Font color` → **Light green** |

The editor collapses the list to three pills plus a "+3 others" badge. The remaining addresses
are not in the DOM, any aria-label/title/input value, or the React component state — the client
does not hold them. **Do not delete this rule**; it cannot be rebuilt faithfully.

## There is NO bold and NO font size — verified 2026-09-24

Josh: *"You used to be able to change it, but it doesn't look like that's an option anymore."*
Confirmed in the live dialog. The three modifications are:

| Modification | What it actually offers |
| --- | --- |
| **Font color** | A named palette — Cranberry, Light green, etc. |
| **Font style** | A **typeface** picker, NOT bold: Aptos, Courier New, Lucida Handwriting, Britannic, Comic Sans MS, MS Gothic |
| **Font & background colors** | A 15-swatch palette that fills the row background as well as the text |

So "make them bigger and bolder" cannot be done. The only ways to make a row louder are a
heavier typeface (Britannic) or a background fill — both were explored and **discarded**, and
nothing about bold reached the script.

## Other verified behaviour

- A rule can hold **several conditions** and **several modifications** (`Add condition` /
  `Add modification`), and **one condition can name several people** — so you do not need a
  rule per person.
- The **name is required first**: opening the Condition list with an empty name throws
  "Please enter a name."
- The people field is free text — type the **full address and press Enter**. Clicking the
  suggestion does not commit it.

## How these frames were actually produced — re-derived 2026-09-24

Recorded because it was written down nowhere and had to be brute-forced back out of the
committed frames by searching for the offset that reproduced one pixel-for-pixel.

```
.\production\capture_window.ps1 -Size 1936x1400          # once, before the first grab
.\production\capture_window.ps1 -Name s01_list -OutDir episodes/004-.../frames/raw
python production/prepare_frames.py --in frames/raw --out frames/clean \
       --page-top 128 --modal s05 s06 s07 s08 s09 s10 s11 s12 s13 s14
```

- Raw frames are **1936x1380** — a windowed capture, not fullscreen. The work area caps the
  height, so `-Size 1936x1400` yields 1380.
- **`--page-top 128`** is the row where the page starts, below Chrome's tab strip and address
  bar. Verified exact: re-running `prepare` on `raw/s08_cond.png` at 128 with `--modal`
  reproduces `clean/s08_cond.png` with zero differing pixels. 126 or 130 differ by ~157,000.
- `--modal` applies to every frame with the settings dialog open, i.e. everything except
  `s01_list` and `s15_after`.

**The `Finance` rule was DISABLED for the whole capture and re-enabled afterwards.** This is
not cosmetic and is not optional to reproduce: with it on, Feddeler and Wilson render light
green, and in the committed frames they are blue. Any additional frame captured with `Finance`
enabled will not cut together with the existing ones.
