# Narration — episode 002

The rendered cut (`TMTT-001-Excel-Dynamic-Arrays.mp4`) ships silent with
burned-in captions. This is the voiceover script for it, generated directly from
the video's caption track, so **the timings below are the video's real timings**
— not the estimates in `script.md`.

183 words over 112 seconds — about 98 words per minute, a
deliberately slow, clear pace for a technical demo.

This file is generated. Edit the wording in `render/episode.html` (the
`CAPTIONS` array), then run `python make_narration.py` and re-render the video.

## The fastest path: Clipchamp text to speech

Clipchamp has an AI voiceover generator built in, so you do not have to record
anything or own a microphone.

1. Open the MP4 in Clipchamp and drop it on the timeline.
2. **Record & create → Text to speech.**
3. Pick a language and voice. Preview a few — the voice carries the whole
   episode, so it is worth two minutes of listening. Prefer a calm, mid-paced
   English voice over an enthusiastic one; this is instruction, not marketing.
4. Paste the **continuous read** below, generate, and drop it on the timeline.
5. Nudge the audio clip so the first word lands at 0:02.5, right as the title
   card ends.
6. Adjust **speed** in the properties panel until the read tracks the picture.
   If a line drifts, split the audio clip there and slide the piece.
7. Once the voice is in, decide about captions. The burned-in ones match this
   script word for word, so they are safe to keep. If you would rather use
   Clipchamp's auto-captions, re-render a clean picture first:
   `python render/make_video.py --no-captions`.

Pitch and pace are adjustable, natural pauses are supported, and it handles up
to ten minutes of audio, so a two-minute episode is well inside the limit.

## Continuous read

Paste this whole block into text to speech for one continuous take. It matches
the on-screen captions word for word.

> Welcome to Two-Minute Training Tuesday. Last week this drop-down changed the whole report. Here's what I didn't tell you — I typed those six names in by hand. The feature behind every drop-down in Excel is called Data Validation. Here's the basic way to build one. Allow: List. And for Source, just select the cells your list lives in. That's a working drop-down, and it's how most of ours are built. Now watch it fail. New line on the export. New cost center — Powder Line 3. Back to the report. Open the drop-down. Still six. The export knows about Powder Line 3. The drop-down doesn't, and it will never tell you. So point Source at a formula instead of at cells I typed. SORT and UNIQUE from last week, on the cost center column. Enter. Seven — it read the data, including the row I just added. Same dialog. New Source. O5, hash. This cell and everything the formula spilled into. There it is. Powder Line 3, and I never touched the drop-down. Next week: Outlook. Find any attachment in four seconds.

## Beat-by-beat, with the video's real timings

Use this if you would rather generate one clip per beat and place each at its
timecode. More work, much tighter sync.

| Starts at | Window | Words | Line |
| --- | --- | --- | --- |
| 0.3 | 3.3s | 5 | Welcome to Two-Minute Training Tuesday. |
| 3.8 | 4.6s | 8 | Last week this drop-down changed the whole report. |
| 8.5 | 4.9s | 15 | Here's what I didn't tell you — I typed those six names in by hand. |
| 13.5 | 4.7s | 11 | The feature behind every drop-down in Excel is called Data Validation. |
| 18.3 | 3.0s | 7 | Here's the basic way to build one. |
| 21.4 | 2.6s | 2 | Allow: List. |
| 24.1 | 5.4s | 11 | And for Source, just select the cells your list lives in. |
| 30.6 | 5.4s | 12 | That's a working drop-down, and it's how most of ours are built. |
| 38.0 | 2.4s | 4 | Now watch it fail. |
| 40.5 | 5.9s | 12 | New line on the export. New cost center — Powder Line 3. |
| 50.0 | 4.4s | 7 | Back to the report. Open the drop-down. |
| 54.5 | 7.5s | 18 | Still six. The export knows about Powder Line 3. The drop-down doesn't, and it will never tell you. |
| 63.5 | 5.0s | 12 | So point Source at a formula instead of at cells I typed. |
| 68.6 | 5.9s | 11 | SORT and UNIQUE from last week, on the cost center column. |
| 79.5 | 6.0s | 13 | Enter. Seven — it read the data, including the row I just added. |
| 85.6 | 4.3s | 4 | Same dialog. New Source. |
| 90.0 | 7.0s | 10 | O5, hash. This cell and everything the formula spilled into. |
| 97.5 | 5.9s | 12 | There it is. Powder Line 3, and I never touched the drop-down. |
| 107.7 | 4.3s | 9 | Next week: Outlook. Find any attachment in four seconds. |

## If you would rather record it yourself

A human voice beats synthesis for internal comms, because people recognise a
colleague and trust it more.

1. Open the MP4 in Clipchamp, **Record & create → Audio.**
2. Watch the picture and read the lines above as each beat arrives. Do not chase
   the timings on the first pass — get a clean read, then slide the audio.
3. When you fumble, pause two seconds and redo the sentence. The silence is
   visible in the waveform, so the retake is trivial to cut.
4. Use a headset mic, not the laptop mic, and close the door.

See [`../../production/recording-sop.md`](../../production/recording-sop.md) for
the full audio setup.

## Also here

`TMTT-001-captions.srt` — the same caption track as a sidecar file, from the same
source. Useful if you upload somewhere that wants captions separately, or want to
edit the wording without re-rendering the video.
