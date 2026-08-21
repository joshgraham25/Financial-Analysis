# Narration — episode 001

The rendered cut (`TMTT-001-Excel-Dynamic-Arrays.mp4`) ships silent with
burned-in captions. This is the voiceover script for it, generated directly from
the video's caption track, so **the timings below are the video's real timings**
— not the estimates in `script.md`.

182 words over 109 seconds — about 100 words per minute, a
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

> Welcome to Two-Minute Training Tuesday. This is an example export file. Three hundred and eighty lines. You need a unique list of the vendors we actually bought from. Instead of copy, paste, Remove Duplicates Here's a better way. One formula: UNIQUE — and the vendor column. Excel writes the table reference for you. Fifteen vendors, out of three hundred and eighty lines. I never told it fifteen. It took exactly the space it needed. Every cell in that list belongs to the one formula in B5. That's a spill range. It isn't sorted — so wrap the whole thing in SORT. One more function around the outside. Nothing else changes. Alphabetical. Still one formula. Now the most powerful one. FILTER — give it the whole table... ...then the rule: cost center equals this cell. A hundred and thirty-six lines — your whole report, sorted by that one filter. Similar to a pivot table. And here's the part that matters. Change the cost center... ...and the whole report redraws itself. No copying. No pasting. No re-sorting. Next week: how we built that drop-down.

## Beat-by-beat, with the video's real timings

Use this if you would rather generate one clip per beat and place each at its
timecode. More work, much tighter sync.

| Starts at | Window | Words | Line |
| --- | --- | --- | --- |
| 0.3 | 3.3s | 5 | Welcome to Two-Minute Training Tuesday. |
| 3.7 | 3.0s | 6 | This is an example export file. |
| 6.8 | 4.0s | 5 | Three hundred and eighty lines. |
| 11.0 | 3.4s | 12 | You need a unique list of the vendors we actually bought from. |
| 14.5 | 3.8s | 6 | Instead of copy, paste, Remove Duplicates |
| 18.4 | 1.7s | 4 | Here's a better way. |
| 21.0 | 4.5s | 8 | One formula: UNIQUE — and the vendor column. |
| 25.6 | 4.3s | 7 | Excel writes the table reference for you. |
| 30.7 | 5.2s | 9 | Fifteen vendors, out of three hundred and eighty lines. |
| 36.0 | 5.4s | 12 | I never told it fifteen. It took exactly the space it needed. |
| 41.5 | 4.9s | 12 | Every cell in that list belongs to the one formula in B5. |
| 46.5 | 2.7s | 4 | That's a spill range. |
| 49.3 | 5.2s | 11 | It isn't sorted — so wrap the whole thing in SORT. |
| 54.6 | 4.3s | 9 | One more function around the outside. Nothing else changes. |
| 59.7 | 3.8s | 4 | Alphabetical. Still one formula. |
| 63.6 | 3.1s | 5 | Now the most powerful one. |
| 66.8 | 6.2s | 7 | FILTER — give it the whole table... |
| 73.1 | 7.8s | 8 | ...then the rule: cost center equals this cell. |
| 82.0 | 5.5s | 14 | A hundred and thirty-six lines — your whole report, sorted by that one filter. |
| 87.6 | 3.3s | 11 | Similar to a pivot table. And here's the part that matters. |
| 91.6 | 3.9s | 4 | Change the cost center... |
| 97.0 | 4.5s | 6 | ...and the whole report redraws itself. |
| 101.6 | 3.9s | 6 | No copying. No pasting. No re-sorting. |
| 105.9 | 3.2s | 7 | Next week: how we built that drop-down. |

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
