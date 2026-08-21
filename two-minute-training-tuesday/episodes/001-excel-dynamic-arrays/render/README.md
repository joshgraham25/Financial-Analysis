# Rendered cut — episode 001

`../TMTT-001-Excel-Dynamic-Arrays.mp4` was generated from this folder rather than
screen-recorded. 1920×1080, H.264, 20 fps, 1:49, about 5.1 MB.

**It has burned-in captions and no voiceover.** Three ways to close that gap,
easiest first:

- **Generate one from here.** `python ../make_voiceover.py` writes a voiced MP4
  beside this one. See below -- this is the recommended path.
- **Ship it silent.** A captioned screencast is a legitimate format, and most
  people watch internal video muted at their desk anyway.
- **Record narration over it.** Open the MP4 in Clipchamp, use *Record → Audio*,
  and read the **Say** column of [`../script.md`](../script.md) against the
  picture. The timings in the script match this cut. Once you add voice, delete
  the burned-in captions and use Clipchamp's auto-captions instead, so the
  captions match what you actually said. A colleague's real voice still beats
  synthesis for internal comms.

## Voiceover, without touching a timeline

[`../make_voiceover.py`](../make_voiceover.py) reads the 22-beat table out of
[`../narration.md`](../narration.md) -- generated from this video's own caption
track -- synthesizes each line, places it at its exact timecode, and muxes the
result onto the picture with `-c:v copy`, so the video is never re-encoded.

```
pip install edge-tts
python ../make_voiceover.py                                # Edge neural, Andrew
python ../make_voiceover.py --voice en-US-AriaNeural
python ../make_voiceover.py --engine sapi --voice David     # offline preview
python ../make_voiceover.py --list-voices
```

Output is `../TMTT-001-Excel-Dynamic-Arrays-voiced-<voice>.mp4`. These are
derived files -- regenerate them, do not edit or commit them.

Two engines. `edge` is Microsoft's neural voices, the same family Clipchamp
offers, and needs outbound network. `sapi` is the David/Zira voices already on
every Windows box: offline, instant, and audibly synthetic -- good for hearing
the pacing in seconds, not for publishing.

**Why not just use Clipchamp's text to speech?** You can, and
[`../narration.md`](../narration.md) has the continuous read ready to paste. But
Clipchamp gives you one long clip to nudge into place by hand, and re-nudge every
time a timing changes. This script places all 22 beats at the timecodes the
picture actually uses, and it is repeatable. Clipchamp cannot be handed a script
or a timing file -- its TTS box takes pasted text and nothing else.

### When a beat overruns

Each line is sped up only as far as its window demands, capped at `--max-rate`
(default 20%), and anything that still does not fit is left long and listed at
the end of the run. That is a **writing** problem, not a voice problem: shorten
the caption in the `CAPTIONS` array in `episode.html`, re-run
`python ../make_narration.py`, then re-render the video and the voiceover.

As of the CLC-palette re-render, three lines are tight -- the 13.3s
copy-paste-dedupe line worst of all, at 15 words in 2.7 seconds.

### Getting a voiced cut into Clipchamp

You often do not need to. The voiced MP4 has both streams muxed and is
publishable as-is. Import it only to edit -- the optional cold open in
[`../script.md`](../script.md), a trim, or swapping the burned-in captions for
Clipchamp's auto-captions. Drag it onto the timeline and the audio comes with the
clip; there is nothing left to sync.

## Regenerating it

```
pip install openpyxl playwright
python make_video.py
```

Needs an ffmpeg with libx264 on `PATH` — the one bundled with Playwright is
VP8-only and will not produce an MP4.

- `episode.html` — the whole video. A canvas renderer with one entry point,
  `drawFrame(t)`, that paints the complete frame for time `t` in seconds. It
  fakes the Excel UI (chrome, formula bar, grid, spill borders, validation
  dropdown, pointer) and draws the caption track.
- `make_video.py` — reads the real 380 rows out of `../demo-workbook.xlsx`,
  injects them into the page, walks the timeline pulling each frame off the
  canvas, and hands the sequence to ffmpeg.

Nothing depends on wall-clock time or randomness, so the same inputs always
produce the same video. To preview single moments without a full render:

```
python make_video.py --probe 24,42,80,96 --outdir /tmp/probe
```

## Changing it

- **Timings** live in the `T` object at the top of `episode.html`. Every scene
  boundary is one number.
- **Captions** are the `CAPTIONS` array — `[start, end, text]`.
- **Pointer path** is the `CURSOR` array — `[t, x, y]`, eased between keyframes.
- **Data** comes from the workbook, so regenerating the workbook regenerates the
  video's contents. Do not hand-edit rows into the HTML.

Runtime is 1:49 against the format's 1:45 target and 2:00 ceiling. If you cut
the `FILTER` section to make it two episodes (see the scope note in
`../script.md`), stop the timeline at `T.scrollRight` and move the recap card up.
