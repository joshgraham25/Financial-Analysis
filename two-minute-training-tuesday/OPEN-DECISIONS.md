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

### 2. Episode 002 — done, awaiting upload

→ **Recorded by Josh 2026-09-08 in real Excel, cut with the new overlay pipeline** (1:43,
`TMTT-002-Self-Maintaining-Dropdowns.mp4`). The synthetic render is retired. **Blocked on
one thing only: the file needs uploading to SharePoint**, because the connector available
here caps uploads at 1 MB and the video is 6 MB. Once it is up, its item URL goes in
`episodes.json` as `videoUrl` — the weekly job refuses to send an episode with an empty
one rather than mailing a dead link.

### 3. Episode 003 — scripted, ready to record

→ **Search Folders in Outlook**, "The Outlook folder that fills itself". Scripted
2026-09-08: shot list in `episodes/003-outlook-search-folders/script.md`, lines to read in
`lines.md`, catalogue entry added. Replaces the attachment-search episode the backlog had
listed — 002's outro already promises Search Folders, and attachment search folds in as
one of the demo criteria. Read the privacy section at the top of the script before
recording: unlike Excel with a generated workbook, this is a tour of a real mailbox.

### 4. A Spanish version — ON HOLD

→ **Josh, 2026-09-08: on hold until somebody asks about it.** The work is done and sitting
in the repo — `TMTT-001-ES-Listas-Sin-Duplicados.mp4`, Spanish captions, Spanish narration,
and `--lang es` through the whole pipeline — so reviving it costs nothing but the two
checks below. Nothing is published and nothing is scheduled.

If it is revived, these still apply, and 4a is the one that decides the size of the job:

**4a. Do the Spanish-speaking staff run Excel in Spanish, or in English?** `Blocked`

Excel localises function names, so the rendered cut shows `=UNICOS`, `=ORDENAR` and
`=FILTRAR`. If their Excel UI is English those formulas return `#¿NOMBRE?` and teach the
wrong thing — `make_video.py --lang en` re-renders with English formulas in minutes, so it
is cheap either way, but it cannot ship until this is known.

**4b. Subtitles or a dubbed voiceover** — settled by building it: the cut is fully dubbed
with `es-MX-JorgeNeural` plus Spanish subtitles. Applies to 001 only; 002 onward are real
recordings, so a Spanish version of those means subtitles or a second take.

**4c. One bilingual email, or two sends?** `Decision` — recommendation stands: one
bilingual email, because a hand-maintained language list is the thing most likely to rot,
which is the same reason the recipient list became `AllUsers@`.

**Also needed regardless:** a native speaker to review the Spanish before it goes
company-wide. Machine-assisted translation is fine for a draft and not fine for the first
thing the whole company reads in Spanish.

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
