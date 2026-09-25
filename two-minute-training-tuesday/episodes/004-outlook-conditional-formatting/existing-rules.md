# Conditional formatting rules — state of Josh's mailbox

## READ THIS FIRST — `Finance` was deleted by me, 2026-09-25

**I deleted Josh's `Finance` rule by accident and it cannot be rebuilt faithfully.** He has
asked to fix it himself later. Until he does, this is the record of what it was.

| | |
| --- | --- |
| **Name** | `Finance` (he had renamed it from `John/Thommy/Caleb`) |
| **Condition** | `From` |
| **Formatting** | `Font color` → **Light green** |
| **People** | `ThomasFeddeler@` · `JohnPiebenga@` · `JenniferWilson@` **plus three the UI never showed** |

The editor collapsed the list to three pills and a "+3 others" badge, and those addresses were
not in the DOM, any aria-label, any input value, or the React state — the client simply did not
hold them. The old name suggests one of the three is a **Caleb**; the connector here lacks
`People.Read`, so that could not be checked.

**How it happened, because the mechanism matters more than the apology.** I looked up the three
delete buttons by element reference, deleted one rule, then clicked the second reference. The
list had re-rendered in between, so that reference no longer pointed where it had, and the
confirmation dialog says only "Are you sure you want to delete this rule?" — it never names the
rule, so there was no checkpoint. All three rules ended up deleted.

**The rule for next time: never chain two destructive clicks off one lookup.** Re-read the list
between them and confirm the target by name, or do them one per page load. The same
stale-reference hazard applies to any list UI that re-renders after a write.

## Current state, after the 2026-09-25 capture

| Rule | State |
| --- | --- |
| `Copied in` | **Live.** Mine, built on camera for the episode — `I'm not on the To line` → Font color Silver. Josh can delete it; nothing depends on it. |
| `Stephen/Abe` | **Live.** Rebuilt on camera, identical to the original: `From` → `sgeist@` + `AbrahamNorton@` → Font color **Cranberry**. |
| `Finance` | **GONE.** See above. |

## There is NO bold and NO font size — verified 2026-09-24

Josh: *"You used to be able to change it, but it doesn't look like that's an option anymore."*
Confirmed in the live dialog, and now stated in the episode itself. The three modifications are:

| Modification | What it actually offers |
| --- | --- |
| **Font color** | A fixed set of named colors — Cranberry, Light green, Silver, Beige, Charcoal … |
| **Font style** | A **typeface** picker, NOT bold: Aptos, Courier New, Lucida Handwriting, Britannic, Comic Sans MS, MS Gothic |
| **Font & background colors** | The same palette, filling the row background as well as the text |

## Other verified behaviour

- A rule can hold **several conditions** and **several modifications**, and **one condition can
  name several people** — so you do not need a rule per person.
- The **name is required first**: opening the Condition list with an empty name throws
  "Please enter a name."
- The people field is free text — type the **full address and press Enter**. Clicking the
  suggestion does not commit it.
- Rules run **top to bottom** and the first match wins. A newly saved rule lands at the **top**
  of the list, not the bottom.
- A rule can be **switched off** with its toggle instead of deleted.

## Hydration — the trap that caused two wrong answers

**A newly saved rule does not apply to the message list until the client re-hydrates**, and a
plain browser reload is not enough: the list renders with *no* conditional formatting at all
until a Settings page load restores it. Worse, the pre-existing rules can be rendering
correctly while a just-saved one is not — so the view looks live and healthy while giving a
false negative.

That is exactly how I twice concluded, wrongly, that `I'm not on the To line` matched nothing.
**Always re-open Settings, close it, wait, and confirm a known row is colored before believing
any negative result.**

## How these frames were produced — 2026-09-25 re-capture

```
.\production\capture_window.ps1 -Fullscreen        # once; F11 at the OS level
.\production\capture_window.ps1 -Name s01_list -OutDir episodes/004-.../frames/raw
python production/prepare_frames.py --in frames/raw --out frames/clean \
       --page-top 0 --fullscreen --modal s05 s06 s07 s08 s09 s10 s11 s12 s13 s14 s16 s17 s18 s19
```

Fullscreen gives exactly **1920x1080** with no browser chrome, so nothing is cropped, padded or
rescaled — prefer it over the windowed `-Size` mode, whose height the work area caps differently
on different monitors. `--fullscreen` selects the mask geometry for that layout; the windowed
constants miss.

**The earlier windowed capture** (superseded) was `-Size 1936x1400` with `--page-top 128`, and
`Finance` disabled throughout so Feddeler and Wilson rendered blue rather than light green.
