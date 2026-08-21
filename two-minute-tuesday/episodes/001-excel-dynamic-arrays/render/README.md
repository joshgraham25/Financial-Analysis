# Rendered cut — episode 001

`../TMT-001-Excel-Dynamic-Arrays.mp4` was generated from this folder rather than
screen-recorded. 1920×1080, H.264, 20 fps, 1:47, about 4.3 MB.

**It has burned-in captions and no voiceover.** That is the one thing it is
missing against the script. Two ways to close that gap:

- **Ship it as-is.** A silent captioned screencast is a legitimate format, and
  most people watch internal video muted at their desk anyway.
- **Record narration over it.** Open the MP4 in Clipchamp, use *Record → Audio*,
  and read the **Say** column of [`../script.md`](../script.md) against the
  picture. The timings in the script match this cut. Once you add voice, delete
  the burned-in captions and use Clipchamp's auto-captions instead, so the
  captions match what you actually said.

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

Runtime is 1:47 against the format's 1:45 target and 2:00 ceiling. If you cut
the `FILTER` section to make it two episodes (see the scope note in
`../script.md`), stop the timeline at `T.scrollRight` and move the recap card up.
