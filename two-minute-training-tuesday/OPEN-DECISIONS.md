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

### 1. The weekly email does not reach the distribution group `Blocked`

**Episode 002 was sent on 2026-09-08 and almost nobody received it.** Found by Josh on
2026-09-10, two days later, because a colleague mentioned it. Nothing in the Hub reported a
problem: the draft is marked `Sent`, `Error` is null, and no bounce arrived.

**What is actually happening.** The message carries the sender on `To` and every real
recipient on `Bcc` — that is the reply-all fix from 2026-09-01. One message went out:

| Recipient | Header | Delivered |
| --- | --- | --- |
| Josh | `To` | **yes** |
| `AllUsers@creativeliquidcoatings.com` (everyone) | `Bcc` | **no** |

So Exchange accepted the message, delivered the `To` copy, and dropped the group expansion.
Because the same message reached a mailbox fine, this is **not** the message being spam
filtered — the only thing that differs is the recipient *type*.

**Why the group specifically.** The Hub sends by **direct send**: unauthenticated SMTP on
port 25 to `creativeliquidcoatings-com.mail.protection.outlook.com`, no credentials by
design (it is how OTP codes go out). Exchange distribution groups default to
`RequireSenderAuthenticationEnabled = $true`, which rejects unauthenticated senders. Direct
send is unauthenticated. 001 worked because it went to seven **individual mailboxes**, which
have no such gate.

**Not yet confirmed, and it needs Exchange admin:** a **message trace** for 2026-09-08
16:10 UTC, from `JoshGraham@` to `AllUsers@`, will say in one line whether it was blocked at
group expansion. Also worth checking the Defender quarantine. Neither console is reachable
from a session here.

**The trap that hid it, and will hide it again.** Josh is on the `To` line of every send by
design, so **his own copy arrives whether or not anyone else's does**. His inbox can never
confirm delivery. Two days of "it went out fine" came from exactly that.

**The three fixes:**

1. **Authenticated submission instead of direct send** — SMTP AUTH as a real mailbox, or
   Graph `sendMail` with an app registration. Satisfies the group's sender-authentication
   requirement, and brings DKIM with it, which helps deliverability generally. Costs an app
   registration or a licensed mailbox, and a change to the sender slice.
2. **Have IT set `RequireSenderAuthenticationEnabled $false` on `All_Users`** — one flag,
   done in minutes. But it also opens a company-wide group to **external** senders, which is
   a standing spam and phishing surface in exchange for fixing one weekly email.
3. **Go back to individual addresses on `Bcc`** — proven to work (001 reached all seven).
   But it reinstates the hand-maintained list that rots and keeps mailing people after they
   leave, which is the thing `AllUsers@` was adopted to remove.

**Recommendation: (1), with (3) as the stopgap for one week if 003 is ready before (1) is.**
(2) trades a permanent security hole for a temporary convenience, on a group that reaches
everyone.

**Regardless of which fix:** the admin page says `Sent` when it means *accepted for
delivery*. That mislabel is what made a silent failure look like a success — worth renaming,
and worth a one-line note under the button.

→ *(open — needs the trace, then a pick from the three)*

### 1b. Verifying a send from now on

Josh's own copy proves nothing (see above). Until delivery is fixed and proven, confirm each
week by asking **one person who is not Josh** whether it arrived — or check a shared mailbox
that is on the group.

→ *(open — could be automated later by Bcc-ing a mailbox a session can read)*

### 2. Episode 002 — published, and delivered by hand

→ **Recorded by Josh 2026-09-08 in real Excel, cut with the new overlay pipeline** (1:43,
`TMTT-002-Self-Maintaining-Dropdowns.mp4`). The synthetic render is retired. Uploaded to
SharePoint the same day, `videoUrl` set, the Hub manifest deployed, and the email sent at
16:10 UTC.

**It reached almost nobody** — see item 1. Josh forwarded it by hand on 2026-09-10 with a
note explaining the delay, which is how the company actually received it. The episode itself
is done and correct; the delivery path is what is broken.

Worth keeping: most of the company had seen **neither** 001 nor 002 before that forward, since
001 only ever went to the seven-person pilot. The forward was most people's first contact with
the series, so it carried a short "what this is, and it is safe to open" line rather than only
an apology.

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

### 6. Where the series stands, 2026-09-24 `Decision`

Written before a context compaction so none of this depends on conversation memory.

**Done and on disk**

- **Renamed to `Two-Minute Training`** — no longer pinned to Tuesday (Josh, 2026-09-23). 17
  files. Published 001/002, the launch announcement and the settled history here were
  deliberately NOT rewritten: they really did go out under the old name.
- **Outros say "Next up:"** rather than "Next week", for the same reason.
- **US spelling throughout** (Josh, 2026-09-24) — the trigger was a caption reading "Font
  colour" over a dialog that says "Font color". 15 files.
- **004 is rendered**: 1:15, real Outlook, `Stephen/Abe` rebuilt on camera, mailbox restored,
  content reviewed frame by frame. Its frames ARE kept in the repo, so any rewording is a
  re-render, not a re-record.

**Open, in the order they block things**

1. **003 is three changes behind** — old series name, "next week", British spelling. All fixed
   in its script, none in its video, because its frames were swept from the scratchpad before
   they were committed. Either re-capture it once (most of a session) or ship it as the last of
   the old name. → 
2. **Re-capture 004 to demo the Cc rule?** Confirmed possible — see `demo-folder-contents.md`:
   two of six rows fade under `I'm not on the To line`. Would take 004 from 1:15 to about 2:00
   and give the "first rule to match wins" line something real to point at. The 1:15 cut is
   finished and correct without it. → 
3. **Nothing is committed** — the rename, the spelling sweep, 004 + frames, the three rebuilt
   production scripts (`capture_window.ps1`, `prepare_frames.py`, `assemble_capture.py`), the
   004 records, the backlog renumber. 003 is also still on branch `003-search-folders-render`,
   unmerged, and the improved 002 re-encode is still uncommitted. → 
4. **Delivery is still the real blocker** — see item 1. Two finished episodes are queued behind
   an email path that does not reach the distribution group.

## Settled

Kept because the reasoning is the useful part, and because a later session will otherwise re-litigate
these.

### Episode 003 — which Outlook, and the first take

**Asked and answered inside a day, 2026-09-17.** I opened this as a question after reading the
first take as classic Outlook — the File tab misled me. It is **new Outlook**: the take shows
`Settings → Mail → Search folders → New search folder`, with the Type dropdown and the
*Filter to specific folders* checkbox. The scripted path was correct all along, so there was
nothing for Josh to decide.

**The take itself could not be used**, for reasons that were all setup rather than performance:
the demo folder was built on a person, so the results list showed external order disputes,
tariff figures and invoice numbers, legibly, with preview text on — on a video bound for a
company-wide library. Alongside that: whole desktop captured instead of the Outlook window,
Calendar pane holding a quarter of the frame, and 100% UI at 1920x1080, which is the same
~11px message list that got 002 reported as blurry. The narration was fine.

**What came out of it.** `recording-setup.md` is a pre-flight checklist built from those exact
failures, and the script and lines were rewritten around the sequence Josh actually performed
— which was better than the original: naming the folder, opening the type list, the folder
filter, and a closing look at the search folders he already keeps. Demo content moved to the
training-words folder, which matches internal mail by construction.

### The distribution group — it exists, and it is `All_Users`

The pilot list of seven hand-listed addresses was replaced by
`AllUsers@creativeliquidcoatings.com` (display name `All_Users`), a real Exchange
distribution group that other company-wide senders already use. That closed the original
question — nothing company-wide until it is a real group.

**But adopting it introduced the failure in item 1.** A group is not a mailbox: it has a
sender-authentication gate that individual mailboxes do not. The list stopped rotting and
started silently not delivering. Both facts are worth holding at once.

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
