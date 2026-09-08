"""Turn Josh's own narration into a beats.md, then let Andrew speak it.

The workflow this exists for (Josh's idea, 2026-09-08):

  1. Record the screen while talking through the script in your own voice.
  2. This script finds where each spoken line starts, by detecting the silences
     between them, and pairs those times with the script's caption lines.
  3. overlay_episode.py then burns the captions and speaks them in Andrew's
     voice at exactly those times, replacing your scratch audio.

So your voice is the metronome and never ships. Nothing has to be timed by hand,
and if a line lands badly you re-record that stretch rather than nudging clips
along a timeline.

    python beats_from_speech.py --video raw-recording.mp4 --lines lines.md
    python beats_from_speech.py --video raw.mp4 --lines lines.md --threshold -30

`--lines` is one caption per line, in the order you said them. Blank lines and
leading markdown bullets or table pipes are ignored, so you can paste the Say
column straight out of script.md.

The one rule while recording: **pause about a second between lines**, and do not
pause in the middle of one. That pause is the whole signal.

Output is <episode folder>/beats.md, ready for overlay_episode.py.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

# ffmpeg prints these to stderr, one pair per silent stretch.
SIL_START = re.compile(r"silence_start:\s*([\d.]+)")
SIL_END = re.compile(r"silence_end:\s*([\d.]+)")


def die(msg: str) -> None:
    sys.exit(f"error: {msg}")


def duration(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(path)],
        capture_output=True, text=True, check=True).stdout.strip()
    return float(out)


def all_silences(video: Path, threshold: int) -> list[tuple[float, float]]:
    """Every pause of 0.2s or more, in one pass.

    Detecting once and filtering in Python is what makes calibration cheap: the
    audio is decoded a single time no matter how many thresholds we try.
    """
    proc = subprocess.run(
        ["ffmpeg", "-hide_banner", "-i", str(video),
         "-af", f"silencedetect=noise={threshold}dB:d=0.2",
         "-f", "null", "-"],
        capture_output=True, text=True)
    starts = [float(m) for m in SIL_START.findall(proc.stderr)]
    ends = [float(m) for m in SIL_END.findall(proc.stderr)]
    if not starts and not ends:
        die("no silences found. Either the recording has no audio track, or the "
            "threshold is wrong -- try --threshold -30 (less strict) or -45 (more).")
    total = duration(video)
    if len(ends) < len(starts):          # trailing silence runs to the end
        ends = ends + [total]
    return list(zip(starts, ends))


def spans_for_gap(silences, total: float, min_gap: float) -> list[tuple[float, float]]:
    """Speech stretches, treating only pauses >= min_gap as line breaks."""
    breaks = [(a, b) for a, b in silences if b - a >= min_gap]
    spans, cursor = [], 0.0
    for a, b in breaks:
        if a > cursor + 0.05:
            spans.append((cursor, a))
        cursor = max(cursor, b)
    if cursor < total - 0.05:
        spans.append((cursor, total))
    return spans


def calibrate(silences, total: float, want: int):
    """Find the pause length that splits the audio into exactly `want` lines.

    Returns (gap, spans). Prefers the largest workable gap -- a bigger pause is a
    more deliberate signal, so it is less likely to have split a line by accident.
    """
    candidates = []
    g = 1.60
    while g >= 0.25:
        spans = spans_for_gap(silences, total, g)
        if len(spans) == want:
            candidates.append((g, spans))
        g = round(g - 0.05, 2)
    return candidates[0] if candidates else (None, None)


def read_lines(path: Path) -> list[str]:
    out = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or set(line) <= set("-| "):
            continue
        line = re.sub(r"^[-*>]\s+", "", line)          # markdown bullets
        if line.startswith("|"):                       # a script.md table row
            cells = [c.strip() for c in line.strip("|").split("|")]
            line = max(cells, key=len)                 # the Say column
        line = re.sub(r"^#+\s+", "", line)
        line = line.strip().strip('"')
        if line:
            out.append(line)
    if not out:
        die(f"{path.name} has no usable lines")
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--video", required=True, help="the recording with your scratch narration")
    ap.add_argument("--lines", required=True, help="one caption per line, in spoken order")
    ap.add_argument("--out", default=None, help="where to write beats.md (default: next to the video)")
    ap.add_argument("--threshold", type=int, default=-35,
                    help="dB below which counts as silence (default -35; -30 is less strict)")
    ap.add_argument("--min-gap", type=float, default=None,
                    help="shortest pause that separates two lines. Omit to calibrate "
                         "it from the script's line count, which is usually right.")
    ap.add_argument("--loose", action="store_true",
                    help="proceed even when the counts differ, pairing as far as they match")
    args = ap.parse_args()

    video = Path(args.video)
    if not video.exists():
        die(f"not found: {video}")
    lines = read_lines(Path(args.lines))
    total = duration(video)
    silences = all_silences(video, args.threshold)

    if args.min_gap:
        gap = args.min_gap
        spans = spans_for_gap(silences, total, gap)
    else:
        gap, spans = calibrate(silences, total, len(lines))
        if gap is None:
            gap = 0.6
            spans = spans_for_gap(silences, total, gap)
            print(f"could not find a pause length giving exactly {len(lines)} "
                  f"lines; showing {gap}s")
        else:
            print(f"calibrated: a pause of {gap:.2f}s or more separates lines")

    print(f"{len(spans)} spoken stretches detected, {len(lines)} script lines")
    if len(spans) != len(lines) and not args.loose:
        print("\nThese have to match, and they don't. Most likely one of:")
        print("  - a pause inside a line split it in two")
        print("  - two lines ran together with no pause between them")
        print("  - the threshold is off (try --threshold -30, or -45)")
        print("\nDetected stretches:")
        for i, (a, b) in enumerate(spans, 1):
            print(f"  {i:2d}. {a:6.2f}s -> {b:6.2f}s  ({b - a:.1f}s)")
        print("\nScript lines:")
        for i, line in enumerate(lines, 1):
            print(f"  {i:2d}. {line[:70]}")
        die("counts differ. Fix the pairing, or re-run with --loose to accept it.")

    pairs = list(zip(spans, lines))
    out_path = Path(args.out) if args.out else video.parent / "beats.md"
    body = [
        "# Caption beats",
        "",
        "Generated by `production/beats_from_speech.py` from Josh's own scratch",
        "narration: each start time is where he actually started saying that line, so",
        "Andrew's read lands on the same action. Times are the RECORDING's clock.",
        "",
        f"Source: `{video.name}`  ·  threshold {args.threshold} dB  ·  pause >= {gap:.2f}s",
        "",
        "| Start | Text |",
        "| --- | --- |",
    ]
    for (start, end), line in pairs:
        body.append(f"| {start:.1f} | {line} |")
    out_path.write_text("\n".join(body) + "\n", encoding="utf-8")

    print(f"\nwrote {out_path}")
    for (start, end), line in pairs:
        print(f"  {start:6.1f}s  ({end - start:4.1f}s spoken)  {line[:58]}")
    print("\nNext:")
    print(f"  python production/overlay_episode.py --episode <n> --video {video.name} --check")


if __name__ == "__main__":
    main()
