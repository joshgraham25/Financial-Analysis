# Narration — episode 001

The rendered cut (`TMT-001-Excel-Dynamic-Arrays.mp4`) ships silent with
burned-in captions. This is the voiceover script for it, generated directly from
the video's caption track, so **the timings below are the video's real timings**
— not the estimates in `script.md`.

179 words over 103 seconds — about 104 words per minute, a
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

> This is a job cost export out of the ERP. Three hundred and eighty lines. Every month. You need the list of vendors we actually bought from. Copy the column, new tab, Remove Duplicates, sort — then do it again next month. Here's the version that never needs doing twice. One formula: UNIQUE — and the vendor column. Excel writes the table reference for you. Fifteen vendors, out of three hundred and eighty lines. I never told it fifteen. It took exactly the space it needed. Every cell in that list belongs to the one formula in B5. That's a spill range. It isn't sorted — so wrap the whole thing in SORT. One more function around the outside. Nothing else changes. Alphabetical. Still one formula. Now the useful one. FILTER — give it the whole table... ...then the rule: cost center equals this cell. A hundred and thirty-six lines. Every one charged to Powder Line 1. And here's the part that matters. Change the cost center... ...and the whole report redraws itself. No copying. No pasting. No re-sorting.

## Beat-by-beat, with the video's real timings

Use this if you would rather generate one clip per beat and place each at its
timecode. More work, much tighter sync.

| Starts at | Window | Words | Line |
| --- | --- | --- | --- |
| 2.5 | 3.0s | 10 | This is a job cost export out of the ERP. |
| 5.6 | 4.0s | 7 | Three hundred and eighty lines. Every month. |
| 10.4 | 2.8s | 10 | You need the list of vendors we actually bought from. |
| 13.3 | 2.7s | 15 | Copy the column, new tab, Remove Duplicates, sort — then do it again next month. |
| 16.1 | 2.3s | 8 | Here's the version that never needs doing twice. |
| 18.5 | 4.5s | 8 | One formula: UNIQUE — and the vendor column. |
| 23.1 | 4.3s | 7 | Excel writes the table reference for you. |
| 28.2 | 5.2s | 9 | Fifteen vendors, out of three hundred and eighty lines. |
| 33.5 | 5.4s | 12 | I never told it fifteen. It took exactly the space it needed. |
| 39.0 | 4.9s | 12 | Every cell in that list belongs to the one formula in B5. |
| 44.0 | 2.7s | 4 | That's a spill range. |
| 46.8 | 5.2s | 11 | It isn't sorted — so wrap the whole thing in SORT. |
| 52.1 | 4.3s | 9 | One more function around the outside. Nothing else changes. |
| 57.2 | 3.8s | 4 | Alphabetical. Still one formula. |
| 61.1 | 3.1s | 4 | Now the useful one. |
| 64.3 | 6.2s | 7 | FILTER — give it the whole table... |
| 70.6 | 7.8s | 8 | ...then the rule: cost center equals this cell. |
| 79.5 | 5.5s | 12 | A hundred and thirty-six lines. Every one charged to Powder Line 1. |
| 85.1 | 3.3s | 6 | And here's the part that matters. |
| 88.5 | 4.5s | 4 | Change the cost center... |
| 94.5 | 4.5s | 6 | ...and the whole report redraws itself. |
| 99.1 | 3.9s | 6 | No copying. No pasting. No re-sorting. |

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

`TMT-001-captions.srt` — the same caption track as a sidecar file, from the same
source. Useful if you upload somewhere that wants captions separately, or want to
edit the wording without re-rendering the video.
