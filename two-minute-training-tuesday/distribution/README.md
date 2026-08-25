# Distribution — how episodes reach the company

Three pieces, decided 2026-08-24:

| Piece | Where it lives | Status |
| --- | --- | --- |
| Video hosting + back catalogue | `CLC Training/Two-Minute Training` on the main site | **LIVE**, read granted, forwarding verified |
| Browse/watch surface | SharePoint itself | Hub section built and deployed, then **HIDDEN** (Josh, 2026-08-25) — SharePoint already is the browse surface |
| Weekly email | Hub **Api** hosted service, drafts on a schedule, **you approve before it sends** | composition BUILT + test-sent (`send_episode_email.py`); scheduling still to do |

The single source of truth for what exists is
[`../episodes.json`](../episodes.json). Both the Hub section and the email job
read it, so a title, runtime, or link is never written down in two places.

---

## Why these three and not something else

**SharePoint hosts the video, not the app.** The app could serve the MP4s, and it
would be worse in every way that matters: no CDN, no adaptive streaming, and
`10.27.11.78` is unreachable off the corporate network — so nobody watches from a
phone at home. SharePoint gives playback, mobile, permissions, and view counts
for nothing. The app links; it does not stream.

**A Hub section, not a new app.** A standalone `clc-tmtt` app would need its own
OTP slice, its own Access Manager registration, its own Caddy route, its own
port, and its own deploy — for what is fundamentally a list of videos. The Hub
already has all of that, already has an audience, and is already where people go
to find internal tools. Every new app is a thing that has to be kept alive.

**Draft-and-hold, not fire-and-forget.** A weekly job that mails the whole
company with no human in the loop will, eventually, mail the whole company
something wrong on a week when nobody was paying attention. The job assembles the
message and parks it; a person clicks send. Once a dozen sends have gone out
uneventfully, revisit — but not before.

---

## The email job, in detail

**It must be a hosted service inside `Clc.DesktopHub.Api`, NOT in the Worker
project.** The Worker project exists but `deploy/deploy.sh` only publishes Api,
so anything registered there never runs in production. The Hub already handles
this exactly once, for `AccessManagerAppLinkSyncWorker` — registered in the Api
process for that stated reason. Follow that precedent; a job in the Worker
project would pass every test and then silently never fire.

Sends through the same Exchange Online direct-send path as `SmtpOtpMailer`, with
its own options section and its own `From`.

**Weekly, Tuesday morning:**

1. Read `episodes.json`. Find the newest episode where `published` is set and no
   send has been recorded.
2. **Refuse to draft if `videoUrl` is empty.** A weekly email whose link 404s is
   worse than no email — it teaches people the series is broken. An episode
   without an uploaded video is not ready, and the job says so in its log rather
   than improvising.
3. Compose from that episode's `summary` plus the SharePoint link. The written
   summary goes **in the message body**, not only in the video: search indexes
   text, not narration.
4. Store the draft and notify the producer. **Nothing is sent.**
5. On approval, send to the configured recipient group, then record the send so
   the same episode is never mailed twice.

**Deliberately not doing:**

- **No hand-maintained recipient list in the app.** A distribution group,
  administered where every other group is. An address list in config rots and
  keeps mailing people who have left.
- **No attachments.** Link to the SharePoint copy. Mailing a 6 MB MP4 to the
  whole company is how you get a talk from IT about mailbox quotas.
- **Not reusing the OTP mailer.** `SmtpOtpMailer` is part of the reviewed OTP
  slice that every app copies verbatim; bending it to carry marketing mail makes
  the next shared-slice fix harder for everyone. Same transport, separate sender.

---

## Ordering

1. **Create the SharePoint library** — a new `Two-Minute Training Tuesday`
   document library on the TFA site (not a folder in the app-data library), plus
   the per-app subfolders and the four columns. No admin needed. Migrating to
   `CLC Training` later is a one-file manifest edit, provided the originals are
   left in place — sent emails cannot be re-pointed.
2. **Upload 001 and 002**, fill in their `videoUrl` and `published` in
   `episodes.json`.
3. **Hub section** — read-only list, newest first, per-app filter, link out to
   SharePoint. Behind the Hub's existing auth; no new access model.
4. **Email job** — draft-and-hold, then the approval surface.
5. **First real send** to a two-person test group before anything company-wide.

Steps 3 and 4 can both be built and tested before step 1 finishes. The job with
no uploaded video simply refuses to draft, which is the behaviour you want to see
in testing anyway.


---

## Settled, with evidence (2026-08-25)

**Links: path-based `stream.aspx`, and forwarding works.** Verified end to end —
an email was forwarded to a colleague who opened the video without being granted
anything. That is the whole point of path-based links over share links: they
authorise against each viewer's own permissions, so there is no per-episode token
to mint, track, or accidentally revoke.

Getting there cost two wrong turns, both recorded so they are not repeated:

1. **A path link on a private library is useless.** While the series sat in the
   TFA library — a private group site with one member — the only thing that
   opened for anyone else was an "anyone in the organisation" share link. A path
   link was substituted for tidiness and broke the first forward. Path links need
   the audience to have read access; check that before choosing the form.
2. **Renaming a published file silently breaks a path link.** The filename is
   encoded in the URL. The Hub keeps rendering a Watch button, the button lands
   on an error, and nothing logs it. `Doc.aspx?sourcedoc={guid}` is rename-proof
   but redirects to the folder listing for video instead of playing, so it is not
   an escape hatch. **Once an episode ships, its published filename is fixed.**

**Mail: no new mailbox needed, and now proven.** Sending as `Two-Minute Training
Tuesday <JoshGraham@…>` — a display name over an address Josh owns — needs no
grant, and a real send **landed in the Inbox** on 2026-08-25 despite the host not
being in CLC's SPF record and there being no DKIM signature. That was the one
genuine deliverability unknown; it is closed. "Mr. Bean" turned out to be the
Hub's existing Finance Assistant persona rather than a mailbox.

**Two defects the first real group send exposed**, both fixed and both now
asserted by tests rather than described in prose:

- Recipients were on the **To** line, so all seven could see each other and one
  Reply All would have hit the list. They go in **Bcc** now, with the sender on
  the To line so the message is not header-less.
- **From** was the shared app-token mailbox the OTP codes use, while the manifest
  documented a real person. Documentation and implementation disagreed and the
  implementation won silently. Sender identity now belongs to the feature's own
  options, and `Reply-To` is set so the footer's "just reply" is true.

**Host gotcha:** `~/.config/clc-shared/smtp.env.sh` uses plain assignments, not
`export`, so sourcing it in a shell does not put `Smtp__Host` in the environment
of a child process. Use `set -a; . file; set +a`.

## Still open

- **Episode 002 is being SCREEN-RECORDED by Josh**, not rendered — the synthetic
  cut was not showing everything he wanted. The script, shot list and generated
  demo workbook all still apply; `render/` is parked, not deleted, and the
  synthetic MP4 in that folder is not the deliverable.
- **001's video cards keep the previous wording** ("Stop copying and pasting") and
  that is FINE — Josh, 2026-08-25. Do not re-render to close the one-word gap: it
  costs a manual upload, a rename and a videoUrl update, for a card on screen a few
  seconds carrying a phrase the narration never speaks.
- **Episode 002 needs substantial rework** before it goes anywhere (Josh,
  2026-08-25). It is rendered and voiced but not uploaded, and should not be.
- **Scheduling the send.** The composition works; the weekly draft-and-hold job
  and its approval step do not exist yet.
- **A recipient distribution group.** Josh is requesting one; until it exists the
  seven-person pilot list in host config stands. It must not stay an address list
  in config.
- **Open decisions live in [`../OPEN-DECISIONS.md`](../OPEN-DECISIONS.md)**, which
  is the durable channel for anything needing Josh rather than code.
