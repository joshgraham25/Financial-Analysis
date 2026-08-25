"""Regenerate narration.md and TMTT-001-captions.srt from the video's caption track.

    python make_narration.py

The caption cues in render/episode.html are the single source of truth: the
video, the narration script, and the SRT all come from the same array, so the
wording and timings cannot drift apart. Edit CAPTIONS in episode.html, re-run
this, and re-render the video.
"""

import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
EPISODE_HTML = HERE / "render" / "episode.html"
NARRATION_MD = HERE / "narration.md"
SRT = HERE / "TMTT-002-captions.srt"


def read_cues():
    src = EPISODE_HTML.read_text(encoding="utf-8")
    block = re.search(r"const CAPTIONS = \[(.*?)\n\];", src, re.S)
    if not block:
        raise SystemExit(f"could not find the CAPTIONS array in {EPISODE_HTML}")
    cues = re.findall(r"\[\s*([\d.]+),\s*([\d.]+),\s*\"(.*?)\"\]", block.group(1))
    if not cues:
        raise SystemExit("CAPTIONS array parsed but held no cues")
    return [(float(a), float(b), t.replace('\\"', '"')) for a, b, t in cues]


def timestamp(sec):
    h, rem = divmod(sec, 3600)
    m, s = divmod(rem, 60)
    return f"{int(h):02d}:{int(m):02d}:{s:06.3f}".replace(".", ",")


def write_srt(cues):
    blocks = [
        f"{i}\n{timestamp(a)} --> {timestamp(b)}\n{text}\n"
        for i, (a, b, text) in enumerate(cues, 1)
    ]
    SRT.write_text("\n".join(blocks), encoding="utf-8")


def write_narration(cues):
    full = " ".join(text for _, _, text in cues)
    words = len(full.split())
    duration = cues[-1][1]
    wpm = round(words / duration * 60)
    rows = "\n".join(
        f"| {a:0.1f} | {b - a:0.1f}s | {len(text.split())} | {text} |"
        for a, b, text in cues
    )
    NARRATION_MD.write_text(TEMPLATE.format(
        words=words, duration=round(duration), wpm=wpm, full=full, rows=rows,
    ), encoding="utf-8")


TEMPLATE = """# Narration — episode 002

The rendered cut (`TMTT-001-Excel-Dynamic-Arrays.mp4`) ships silent with
burned-in captions. This is the voiceover script for it, generated directly from
the video's caption track, so **the timings below are the video's real timings**
— not the estimates in `script.md`.

{words} words over {duration} seconds — about {wpm} words per minute, a
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

> {full}

## Beat-by-beat, with the video's real timings

Use this if you would rather generate one clip per beat and place each at its
timecode. More work, much tighter sync.

| Starts at | Window | Words | Line |
| --- | --- | --- | --- |
{rows}

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
"""


def main():
    cues = read_cues()
    write_srt(cues)
    write_narration(cues)
    print(f"{len(cues)} cues -> {NARRATION_MD.name}, {SRT.name}")


if __name__ == "__main__":
    main()
