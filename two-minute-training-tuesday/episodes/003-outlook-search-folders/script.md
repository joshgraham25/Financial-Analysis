# Episode 003 — The Outlook folder that fills itself

| | |
| --- | --- |
| **Episode** | 003 |
| **App** | Outlook — **new Outlook for Windows** |
| **Tip** | **Search Folders** — a saved search that looks and behaves like a folder |
| **Target runtime** | 2:05 (ceiling 2:30 — Josh, 2026-09-08: "2:00 plus or minus 30 seconds") |
| **Recorded** | Real Outlook, per [`../../production/recording-sop.md`](../../production/recording-sop.md) |
| **Recap card lines** | 1. `Settings → Mail → Search folders` · 2. Mail with specific words · 3. Mail never moves — the tag shows where it lives |

## Which Outlook — confirmed, not assumed

**New Outlook for Windows.** The 2026-09-17 take settles it: Josh drove
`Settings → Mail → Search folders → New search folder`, with the name box, the **Type**
dropdown and a **Filter to specific folders** checkbox. That is the new-Outlook flow, so the
path below is right and does not need re-deciding.

Classic Outlook builds these from the `Folder` ribbon tab with free-form criteria, and
Microsoft is explicit that *"advanced custom Search Folders are supported only in classic
Outlook."* New Outlook offers predefined types instead. **Mail with specific words** does
what this episode needs, so the lesson survives intact.

The types new Outlook offers, since the script name-checks the list:

| Reading mail | Mail from people and lists | Organizing mail |
| --- | --- | --- |
| Unread mail | Sent directly to me | Categorized mail |
| Flagged for follow-up | From specific people | **Mail with attachments** |
| Unread *or* flagged | From and to specific people | **Large mail** |
| Important mail | Sent to public groups | Old mail · **Mail with specific words** |

## Read this before you hit record — Outlook is not Excel

**Everything in this section is now a pre-flight checklist:
[`recording-setup.md`](recording-setup.md). Work through it with the recorder off.**

The short version of why it exists. 002 was safe because the workbook was generated. **Your
mailbox is full of customer and employee names, and this goes to a company-wide library.**
The 2026-09-17 take demonstrated the folder on a person, and the results list showed
external order disputes, tariff figures and invoice numbers — all legible, all with preview
text on. That is not fixable in post, which is why the demo below uses the training-words
folder instead: it matches internal training mail by construction.

## Criteria — tested for real, 2026-09-17

**Built the folder in the live mailbox, looked at it, deleted it.** No longer a question:

- **It searches subject AND body.** The dialog says so outright in step 3: *"Please enter words
  to search for in email subject and body."* That was the open risk.
- **"Two-Minute Training" is clean anyway.** 12 messages, every one of them about the series, no
  junk at all. The hyphenated three-word phrase is distinctive enough to survive a body search,
  where the bare `two minute` was not. **Use these exact words.**
- **The words become a removable tag** when you press Enter, and you can add several. Worth one
  beat on camera.
- **Name before type.** The form refuses to let you choose a type until the folder has a name —
  it throws "Please enter a search folder name". The script follows that order.
- **Label correction:** the person-based type is called *"Mail with specific people"*, not
  "From specific people".

## The proof shot changed — and it got better

**Every row in a Search Folder shows the folder it actually lives in**, as a small tag beside the
date. That is a far stronger proof of "nothing moved" than the original plan of clicking back to
the Inbox: you simply point at the tags.

It also **removes the one shot no setting could sanitise.** The old script needed the live Inbox on
camera, with whatever arrived that morning sitting around the target message. It no longer does.

**What the tags actually say, as of 2026-09-17:** the 12 results come from **Sent Items** and
**Two Minute Tuesday Ideas** — two different folders, one list. Nothing sits in the Inbox right
now, so *"including the ones I never filed"* has no proof on screen and has been cut. The honest
and more visual line is the one the tags support: **three folders at once, and nothing moved.**

**Precision on the catch.** Deleting the *folder* does not delete anything — Outlook says so in its
own confirmation dialog. Deleting a *message* from inside the folder deletes the real message.
The script says message, deliberately.

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

**Act 2 — build it (0:25–1:10).** `Settings → Mail → Search Folders → Create new search
folder → Mail with specific words`. Type the words. Save.

**Act 3 — the part people miss (1:20–2:05).** The new folder holds every matching email,
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
| 0:09 | "Every one of these got here because I moved it by hand." | Scroll the short list |
| 0:14 | "And the ones I never filed are scattered everywhere else." | — |
| 0:19 | "A Search Folder fixes that. It's a folder that fills itself." | Hover the folder list |
| 0:25 | "Settings — the gear, top right." | Click the gear |
| 0:29 | "Mail, then Search folders." | **Mail → Search folders** — the list of existing ones |
| 0:34 | "Add search folder." | The blue **+ Add search folder** button |
| 0:38 | "Name it first — it won't let you go on without one." | The name box |
| 0:43 | "Two-Minute Training." | Type it |
| 0:47 | "Then pick a type. There's a whole list of these." | Open **Type** — let the list sit open a beat |
| 0:53 | "Mail with specific words." | Last item under **Organizing mail** |
| 0:58 | "And the words: Two-Minute Training. Enter, and it becomes a tag." | Type, press Enter, the chip appears |
| 1:05 | "You can limit it to certain folders, or leave it and it searches everything." | Hover **Filter to specific folders** — don't tick it |
| 1:12 | "Save." | Save; the new folder joins the list |
| 1:16 | "There it is, down with the other search folders." | Close settings; the folder in the pane |
| 1:21 | "Twelve messages, from two different folders at once." | The populated list |
| 1:27 | "Here's the part people miss. Look at the tag on each one." | **Slow scroll — the folder tag beside each date is the shot** |
| 1:34 | "Sent Items. My ideas folder. That's where they still live." | Rest on two rows with different tags |
| 1:40 | "Nothing moved. A Search Folder is a saved search, not a place." | — |
| 1:46 | "A rule moves your mail. This one just finds it." | — |
| 1:51 | "So deleting a message from here deletes the real message. That's the one catch." | — |
| 1:58 | "I've got a few of these now — one per project, one per person I trade a lot of mail with." | **The folder pane only — do not open them** |
| — | **Over the recap card:** "That's it for this week." | Recap card |
| — | **Over the recap card:** "Next week: colour-coding your inbox." | Recap card |

The last two lines are prefixed `>` in `captions.md` so they are cut from the picture and
spoken over the card — see 002.

## If it runs long, cut in this order

1. "I've got a few of these now…" — the closing survey of existing folders. It is a nice
   grace note and the riskiest shot in the episode; it goes first.
2. "You can point it at certain folders…" — the folder filter. Useful, not the lesson.
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
