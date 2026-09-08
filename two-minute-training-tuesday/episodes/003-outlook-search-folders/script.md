# Episode 003 — The Outlook folder that fills itself

| | |
| --- | --- |
| **Episode** | 003 |
| **App** | Outlook |
| **Tip** | **Search Folders** — a saved search that looks and behaves like a folder |
| **Target runtime** | 1:45 (ceiling 2:30 — Josh, 2026-09-08: "2:00 plus or minus 30 seconds") |
| **Recorded** | Real Outlook, per [`../../production/recording-sop.md`](../../production/recording-sop.md) |
| **Recap card lines** | 1. `Folder → New Search Folder` · 2. Custom: words in subject or body · 3. Mail never moves — it is a saved search |

## Read this before you hit record — Outlook is not Excel

002 was safe because the workbook was generated. **Your mailbox is full of customer
and employee names, and this goes to a company-wide library.** The whole video is a
tour of your mail.

- **Turn off the reading pane** (`View → Layout → Reading Pane → Off`) so message
  bodies never render. The list alone is enough to teach this.
- **Check the sender and subject columns** in every shot. Those are the two things
  that will be legible, and they are enough to leak a customer dispute or an HR matter.
- Consider a **scratch mailbox folder** with a handful of harmless emails if your real
  Inbox cannot be shown. The lesson does not depend on the mail being real.
- **Hide the screen-share banner** before recording (click **Hide** on it). In 002 it
  sat in every frame with the tenant hostname and had to be painted over in post.
- Zoom: **Outlook's list at 100% is small.** Use `Ctrl+Scroll` in the message list, or
  drop the display resolution, so the folder names and subjects are readable on a phone.

## The pain, in one sentence

> You file the emails you want to find later, so the ones you forget to file are the
> ones you cannot find.

## Why this episode, and why now

It is the same spine as 001 and 002: **stop maintaining by hand something the tool will
maintain for you.** `=UNIQUE` replaced copy-paste-dedupe; `=$M$5#` replaced a typed
list; a Search Folder replaces filing.

It is also genuinely Josh's own problem — the **Two Minute Tuesday Ideas** subfolder he
files idea emails into by hand. Using a real habit rather than an invented scenario is
what made 002's cost-centre drop-down land.

## Structure: the manual habit, the fix, then the thing people get wrong

**Act 1 — the habit (0:00–0:25).** The Ideas folder. Every email in it got there because
he moved it. The ones he forgot are still in the Inbox, unfound.

**Act 2 — build it (0:25–1:05).** `Folder → New Search Folder → Create a custom Search
Folder`. Name it, set the criteria to words in subject or body, browse the whole mailbox
including subfolders. Three OKs.

**Act 3 — the part people miss (1:05–1:35).** The new folder holds every matching email,
*including ones never filed*. Then click one and show it is **still in the Inbox**.
Nothing moved. That is the difference from a rule — a rule moves mail, a Search Folder
finds it. And the catch that follows from it: delete from here and you delete the real
email.

## Shot list

The **Say** column is what to speak while recording. Talk normally and **pause about a
second between lines** — the pause is what lets `recut_from_srt.py` place the captions.
Your voice is the metronome; Andrew speaks the final cut.

| Time | Say | On screen |
| --- | --- | --- |
| 0:00 | "Welcome to Two-Minute Training Tuesday." | Outlook, folder list visible |
| 0:04 | "This folder holds every training idea anyone sends me." | Click **Two Minute Tuesday Ideas** |
| 0:09 | "Every one of these got here because I moved it by hand." | Scroll the list |
| 0:14 | "So the ones I forgot to file aren't here at all." | Back to Inbox |
| 0:19 | "A Search Folder fixes that. It's a folder that fills itself." | Hover the folder list |
| 0:25 | "On the Folder tab — New Search Folder." | `Folder` ribbon tab → **New Search Folder** |
| 0:31 | "Scroll to the bottom. Create a custom Search Folder." | The preset list, then **Custom** |
| 0:37 | "Choose. Name it Training ideas." | Name box |
| 0:43 | "Criteria. The words two minute, in the subject or body." | Criteria dialog |
| 0:51 | "Browse — the whole mailbox, including subfolders." | Browse, tick subfolders |
| 0:58 | "OK, OK, OK." | Three dialogs closing |
| 1:03 | "There it is, under Search Folders." | The new folder, populated |
| 1:09 | "Every email that mentions it — including the ones I never filed." | Scroll: more than the Ideas folder held |
| 1:16 | "Here's the part people miss." | Click one message |
| 1:20 | "That email is still sitting in my Inbox. Nothing moved." | Show its real folder |
| 1:26 | "A Search Folder is a saved search, not a place." | The folder list |
| 1:31 | "That's the difference from a rule. A rule moves mail. This just finds it." | — |
| 1:37 | "So deleting from here deletes the real email. That's the one catch." | — |
| 1:43 | "Unread across every folder. Anything with a big attachment. Everything from your boss." | Preset list again, briefly |
| — | **Over the recap card:** "That's it for this week." | Recap card |
| — | **Over the recap card:** "Next week: Teams, and how to never lose a message again." | Recap card |

The last two lines are prefixed `>` in `captions.md` so they are cut from the picture and
spoken over the card — see 002.

## If it runs long, cut in this order

1. The 1:43 line listing three more Search Folders to build. Nice-to-have, not the lesson.
2. "OK, OK, OK." — the dialogs closing read fine silently.
3. "A Search Folder is a saved search, not a place." — 1:31 makes the same point better.

**Never cut** the "still in my Inbox" beat. That is the episode. Without it people assume
this is a rule that moves their mail, and the first thing they will do is delete from it.

## After recording

```bash
python production/recut_from_srt.py --video raw-recording.mp4 --srt "<clipchamp>.srt" \
    --captions episodes/003-outlook-search-folders/captions.md --out raw-tight.mp4
python production/overlay_episode.py --episode 3 --video raw-tight.mp4 --check
python production/overlay_episode.py --episode 3 --video raw-tight.mp4
```

`captions.md` is written **after** the recording, because it needs one line per cue in
Clipchamp's SRT. [`lines.md`](lines.md) holds the intended wording to read from while
recording; the captions are the tightened version of whatever actually got said.

Also needed before the weekly job will mail it: upload the finished MP4 and put its
SharePoint item URL in `episodes.json` as `videoUrl`. The job refuses to send an episode
with an empty `videoUrl` rather than mailing a dead link.
