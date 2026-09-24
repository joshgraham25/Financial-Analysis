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
