# Episode 003 — The Outlook folder that fills itself

| | |
| --- | --- |
| **Episode** | 003 |
| **App** | Outlook — **new Outlook for Windows** |
| **Tip** | **Search Folders** — a saved search that looks and behaves like a folder |
| **Target runtime** | 1:45 (ceiling 2:30 — Josh, 2026-09-08: "2:00 plus or minus 30 seconds") |
| **Recorded** | Real Outlook, per [`../../production/recording-sop.md`](../../production/recording-sop.md) |
| **Recap card lines** | 1. `Settings → Mail → Search Folders` · 2. Mail with specific words · 3. Mail never moves — it is a saved search |

## Which Outlook — this decides the whole build sequence

**Josh is on new Outlook, so this episode is recorded there.** That is not a detail; the
two clients build Search Folders in completely different places, and an earlier draft of
this script described the classic path, which does not exist for him.

- **Classic Outlook:** `Folder` ribbon tab → New Search Folder → *Create a custom Search
  Folder* → free-form criteria. Powerful, and **not what most of us have.**
- **New Outlook:** Search Folders returned in the March 2026 update, but as **predefined
  types only.** Microsoft: *"Advanced custom Search Folders are supported only in classic
  Outlook."*

The predefined type **Mail with specific words** does what this episode needs, so the
lesson survives intact — only the clicks change.

**Teach the client the audience has.** A tip people cannot follow is worse than a slightly
less powerful one, so the script says one line acknowledging classic can go further.

The types new Outlook offers, since the closing line name-checks three:

| Reading mail | Mail from people and lists | Organizing mail |
| --- | --- | --- |
| Unread mail | Sent directly to me | Categorized mail |
| Flagged for follow-up | From specific people | **Mail with attachments** |
| Unread *or* flagged | From and to specific people | **Large mail** |
| Important mail | Sent to public groups | Old mail · **Mail with specific words** |

## Read this before you hit record — Outlook is not Excel

002 was safe because the workbook was generated. **Your mailbox is full of customer
and employee names, and this goes to a company-wide library.** The whole video is a
tour of your mail.

- **Turn off the reading pane** so message bodies never render. The list alone teaches this.
- **Check the sender and subject columns** in every shot. Those are the two legible things,
  and they are enough to leak a customer dispute or an HR matter.
- **Zoom the message list to 150–175%** (`Ctrl+Scroll`). This is Rule 1 in the SOP: 002 was
  reported blurry because 11px text does not survive SharePoint's 540p rendition.
- **Hide the screen-share banner** before recording. In 002 it sat in every frame carrying
  the tenant hostname and had to be painted over in post.
- **Record the Outlook window, not the whole screen.**

## Test the criteria before you record — twice bitten here

**Unknown and worth five minutes: whether "Mail with specific words" searches the subject
only, or the subject and the body.** Classic Outlook lets you pick; new Outlook's predefined
type does not say.

It matters because searching bodies for `two minute` in Josh's real mailbox returned five
unrelated messages — a Power BI newsletter ("**Two** settings… **two** finance benchmarks"),
an "Introduction to Julia" thread, paint booth specs and an insurance campaign. A Search
Folder full of junk argues against the episode while you are narrating it.

**So: build it once, look at what it catches, delete it, then record building it again.**
If it is noisy, use the fuller phrase **"Two-Minute Training Tuesday"**, which is
distinctive enough to survive a body search.

## The payoff shot is real, and it is in the mailbox already

Athena Lakis replied to 001 with the subject *"RE: Two-Minute Training Tuesday #001 —
training request - remove blanks"* — an actual training request, sitting in the Inbox rather
than the Ideas folder. That demonstrates "including the ones I never filed" with a real
message instead of asserting it. Frame that one when you scroll the results.

Her name and subject line will be legible. It is an internal colleague asking for a tip,
which is harmless — but it is a real person on a company-wide video.

## Proving "nothing moved"

Classic Outlook has an **In Folder** column, which makes this a one-shot proof. New Outlook
may not expose it, so **the script uses a method that works in any client**: select the
message in the Search Folder, then click **Inbox** — the same message is still sitting there.

If your build of new Outlook does show a folder indicator in Search Folder results, use it;
it is faster. Check before recording rather than discovering it mid-take.

## The pain, in one sentence

> You file the emails you want to find later, so the ones you forget to file are the
> ones you cannot find.

## Why this episode, and why now

Same spine as 001 and 002: **stop maintaining by hand something the tool will maintain for
you.** `=UNIQUE` replaced copy-paste-dedupe; `=$M$5#` replaced a typed list; a Search Folder
replaces filing.

It is also genuinely Josh's own problem — the **Two Minute Tuesday Ideas** subfolder he
files idea emails into by hand. A real habit rather than an invented scenario is what made
002's cost-centre drop-down land.

## Structure

**Act 1 — the habit (0:00–0:25).** The Ideas folder. Every email in it got there because he
moved it. The ones he forgot are still in the Inbox, unfound.

**Act 2 — build it (0:25–1:05).** `Settings → Mail → Search Folders → Create new search
folder → Mail with specific words`. Type the words. Save.

**Act 3 — the part people miss (1:05–1:40).** The new folder holds every matching email,
*including ones never filed*. Then click back to the Inbox and show the message is **still
there**. Nothing moved. That is the difference from a rule — a rule moves mail, a Search
Folder finds it. And the catch that follows: delete from here and you delete the real email.

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
| 0:25 | "Settings — the gear, top right." | Click the gear |
| 0:30 | "Mail, then Search Folders." | Settings dialog: **Mail → Search Folders** |
| 0:36 | "Create new search folder." | The button |
| 0:41 | "Under Organizing mail — Mail with specific words." | The type list |
| 0:48 | "The words: Two-Minute Training." | The words box |
| 0:55 | "Save." | Save, settings closes |
| 1:00 | "There it is, under Search Folders." | The new folder in the folder pane, populated |
| 1:06 | "Every email about it — including the ones I never filed." | Scroll past what the Ideas folder held. **Athena's "training request - remove blanks" reply is the proof shot** |
| 1:13 | "Here's the part people miss." | Click that message |
| 1:17 | "Now back to the Inbox. It's still sitting right there. Nothing moved." | Click **Inbox**, the same message is in the list |
| 1:25 | "A Search Folder is a saved search, not a place." | The folder pane |
| 1:30 | "That's the difference from a rule. A rule moves mail. This just finds it." | — |
| 1:36 | "So deleting from here deletes the real email. That's the one catch." | — |
| 1:42 | "There are more ready to go — unread mail, mail with attachments, large mail." | The type list again, briefly |
| 1:48 | "Classic Outlook can build fully custom ones. This is the version most of us have." | — |
| — | **Over the recap card:** "That's it for this week." | Recap card |
| — | **Over the recap card:** "Next week: Teams, and how to never lose a message again." | Recap card |

The last two lines are prefixed `>` in `captions.md` so they are cut from the picture and
spoken over the card — see 002.

## If it runs long, cut in this order

1. The "Classic Outlook can build fully custom ones" line. True and useful, but it is a
   footnote and the episode survives without it.
2. "There are more ready to go…" — the other predefined types. Nice to have, not the lesson.
3. "A Search Folder is a saved search, not a place." The next line makes the same point better.

**Never cut** the "still sitting right there / nothing moved" beat. That is the episode.
Without it people assume this is a rule that moves their mail, and the first thing they will
do is delete from it — which deletes the real message.

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
SharePoint item URL in `episodes.json` as `videoUrl`. **And note the standing blocker in
`OPEN-DECISIONS.md` item 1 — the weekly email currently does not reach the distribution
group at all**, so a perfect 003 still lands nowhere until that is fixed.
