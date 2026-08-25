# Distribution — how episodes reach the company

Three pieces, decided 2026-08-24:

| Piece | Where it lives | Status |
| --- | --- | --- |
| Video hosting + back catalogue | SharePoint library in the **TFA** space | folder to create — [`admin-setup.md`](admin-setup.md) |
| Browse/watch surface | A **section in the existing CLC Desktop Hub** | BUILT on `feat/tmtt-section`, not deployed |
| Weekly email | Hub **Api** hosted service, drafts on a schedule, **you approve before it sends** | to build; sends as Josh for now, Mr. Bean needs Send As |

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

1. **Create the SharePoint folder** — `Two_Minute_Training_Tuesday` in the
   existing Thomas F Anderson Library, plus the per-app subfolders and the four
   library columns. No admin needed; Josh has the access.
2. **Upload 001 and 002**, fill in their `videoUrl` and `published` in
   `episodes.json`.
3. **Hub section** — read-only list, newest first, per-app filter, link out to
   SharePoint. Behind the Hub's existing auth; no new access model.
4. **Email job** — draft-and-hold, then the approval surface.
5. **First real send** to a two-person test group before anything company-wide.

Steps 3 and 4 can both be built and tested before step 1 finishes. The job with
no uploaded video simply refuses to draft, which is the behaviour you want to see
in testing anyway.
