# Open decisions

The durable channel for questions that need Josh rather than code. Edit this file directly — I read
it at the start of a session, so an answer here needs no chat round trip and survives the session
ending.

There is also a clickable version that builds a paste-back block:
<https://claude.ai/code/artifact/d18a8ce9-29e3-4862-9e76-50ad3d28d44f>. Same questions; use whichever
is closer to hand. This file is the record.

**Convention:** answer on the `→` line. Leave the question in place; I move it to Settled once acted
on, with what happened.

---

## Open

### 1. Distribution group

Seven addresses are hand-listed in the Hub's host config. That list rots and will keep mailing people
after they leave, so nothing goes company-wide until it is a real group.

→ **Josh is requesting one.** Waiting on the group's address. Until it exists the pilot list stands.

### 2. Episode 002

→ **Josh is recording it himself** — the synthetic render was not showing everything he wanted. The
script, the shot list and the generated demo workbook all still apply; see the note at the top of
`episodes/002-self-maintaining-dropdowns/script.md`. Nothing for me to do until there is a recording
to publish.

### 3. Episode 003 and beyond

Not started, deliberately: 002 comes first. The backlog has roughly six months of ranked ideas, and
002's outro already promises Outlook attachment search as 003.

→ *(open — say when to script it)*

### 4. A Spanish version — three questions, and one of them changes everything

Josh asked for a Spanish version on 2026-09-01. CLC clearly has the audience: `CLC Training` already
holds *IQMS Training Guides - Spanish* and *Paulson Training Videos - English and Spanish*.

**4a. Do the Spanish-speaking staff run Excel in Spanish, or in English?** `Blocked`

This is the one that changes the size of the job. Excel **localises function names**:

| English | Spanish |
| --- | --- |
| `=UNIQUE(range)` | `=UNICOS(rango)` |
| `=SORT(UNIQUE(range))` | `=ORDENAR(UNICOS(rango))` |
| `=FILTER(table, column = criteria)` | `=FILTRAR(tabla, columna = criterio)` |
| Remove Duplicates | Quitar duplicados |

- **If their Excel UI is Spanish:** a translated video showing `=UNIQUE(...)` teaches a formula that
  returns `#¿NOMBRE?`. The formulas, the recap card, the demo workbook and the on-screen Excel chrome
  all have to change — that is a genuinely different episode, not a translation.
- **If their Excel UI is English:** only the words change. Formulas stay as they are, and this is
  much cheaper.
- **If it is mixed:** say the English formula out loud and show it on screen, because that is what
  their keyboard will accept, and translate only the prose around it.

→ *(open)*

**4b. Subtitles, or a Spanish voiceover?** `Decision`

The pipeline can do either for episode 001. Subtitles are cheap and keep one video; a dubbed version
is a second file, and the neural voices available include Mexican Spanish (`es-MX-JorgeNeural`,
`es-MX-DaliaNeural`), so it would not sound robotic.

Note this only applies to **001**, which is synthetically rendered. **002 onward Josh is recording
himself**, so a Spanish version of those means either subtitles or recording a second take.

→ *(open)*

**4c. One bilingual email, or two separate sends?** `Decision`

- **One email, English then Spanish below it.** Everyone gets one message; nobody is on the wrong
  list; it is visibly one series. Costs length.
- **Two sends to two lists.** Cleaner for each reader, but needs a Spanish-speaker distribution list
  that does not exist yet, and doubles the approval step every week.
- Recommendation: **one bilingual email**, because a list that has to be maintained by hand is the
  thing most likely to rot — the same reason the recipient list became `AllUsers@`.

→ *(open)*

**Also needed regardless:** a native speaker to review the Spanish before it goes company-wide. A
draft is in `distribution/first-announcement.md`; machine-assisted translation is fine for a draft
and not fine for the first thing the whole company reads in Spanish.

---

## Settled

Kept because the reasoning is the useful part, and because a later session will otherwise re-litigate
these.

### Deliverability — resolved 2026-08-25

The first send as a real person over direct send **landed in the Inbox**, not Junk. That was the one
genuine unknown: the host is not in CLC's SPF record and there is no DKIM signature.

**Sender stays `Two-Minute Training Tuesday <JoshGraham@creativeliquidcoatings.com>`.** No new mailbox,
no Send As grant, no `training@` alias needed. Revisit only if replies should go somewhere other than
Josh's inbox, or if the series should outlive his account.

### Episode 001's first send — not being corrected

The copy the group received had all seven recipients on the To line and came from the app-token
mailbox. Both are fixed (Bcc, and a real From), but that message is out and **Josh's call is to leave
it** rather than send a second email about the same episode. Consequence to remember: those six people
hold each other's addresses from that To line.

### The series branch — merged

`claude/weekly-tech-tips-videos-lppg5s` is merged to `main`.

### Fleet vehicle-insurance question — not here

Belongs in the Fleet session, not this one. Untouched.

### Earlier, and still true

- Videos live in SharePoint `CLC Training/Two-Minute Training`; read granted; forwarding verified.
- Links are path-based `stream.aspx` URLs. **A published filename is fixed** — renaming one silently
  breaks the link while the Watch button keeps rendering.
- The Hub's Training catalogue is built but **hidden**: SharePoint is already the browse surface. The
  endpoint, reader, page and tests remain because the email job uses the same catalogue.
- The weekly email drafts Monday 07:00 Eastern and waits for a SuperAdmin to send it. Recipients and
  body are frozen at draft time, so a config or manifest change cannot alter something already
  reviewed.
- 001's video cards keep the older wording ("Stop copying and pasting"). **Do not re-render to fix
  it** — it costs an upload and a rename for a card on screen a few seconds carrying a phrase the
  narration never speaks.
- SharePoint metadata columns were skipped: the folder sits inside the company-wide Shared Documents
  library, so columns there would hit everyone.
