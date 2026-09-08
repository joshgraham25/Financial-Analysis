"""Retime a raw screen recording to the pace of its rewritten captions.

Stage one of the two-stage pipeline. Stage two is overlay_episode.py, which puts
the cards, the burnt-in captions and Andrew's voice on the result.

Why this exists: episode 002's raw take ran 2:25 against a 2:00 ceiling, and only
26 s of that was dead air. The other 119 s was speech -- Josh talking through each
step at roughly twice the length the caption needs. Cutting pauses alone could
never get there, and cutting *content* would lose beats. So instead each spoken
stretch is sped up to exactly as long as Andrew's read of its caption, and the
pauses between them are squeezed. Nothing is removed; the whole demonstration
stays on screen, just at the pace of the words that will actually be heard.

    python recut_from_srt.py --video take2.webm --srt "Video Project 3.srt" \
        --captions episodes/002-.../captions.md --out raw-tight.mp4

Then:

    python overlay_episode.py --episode 2 --video raw-tight.mp4 --check
    python overlay_episode.py --episode 2 --video raw-tight.mp4

Inputs
------
--srt       Clipchamp's auto-caption export. Only its TIMINGS are used -- they
            mark where each spoken stretch begins and ends, which is better than
            deriving them from silence detection.
--captions  The rewritten captions, one per cue, same count and order. Two
            tokens instead of text:
              "-"  keep the picture, drop the caption -- the stretch becomes
                   dead air and is compressed (Clipchamp emits stray fragments
                   like a lone "So").
              "x"  cut the stretch out altogether.
              ">"  cut the stretch from the picture, but keep the line as an
                   OUTRO beat -- spoken over the recap card, which stretches to
                   hold it. Use it for "next week..." so the card arrives while
                   there is still something being said.

--gentle-first N
            Cap the first N spoken stretches at --gentle-speed instead of
            --max-speed. The opening is where a viewer is still working out what
            they are looking at, and sped-up mouse movement there reads as
            jitter rather than pace.
--cover     Region to paint over, as x,y,w,h. Defaults to episode 002's
            "... is sharing your screen" banner, which otherwise appears in
            every frame and puts the tenant hostname in a company-wide video.

Outputs the retimed video, plus a beats.md carrying each caption's NEW start time.

Video only -- the scratch narration is deliberately dropped, since Andrew speaks
the captions in stage two.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

TIME = re.compile(r"(\d+):(\d+):(\d+)[,.](\d+)\s*-->\s*(\d+):(\d+):(\d+)[,.](\d+)")

DEFAULT_VOICE = "en-US-AndrewNeural"
SPEECH_PAD = 0.25       # air after each line before the next segment
DEFAULT_GAP = 0.7       # what a pause between lines is squeezed to
MAX_SPEECH_SPEED = 1.5  # Josh: 2:00 +/- 30s is fine, so retime gently.
                        # Past ~1.5x the cursor starts to look frantic.
GENTLE_FIRST = 7        # Josh's review: the opening felt "rushed and jittery".
GENTLE_SPEED = 1.15     # Nearly real time while the viewer gets oriented.
MAX_GAP_SPEED = 8.0
# Episode 002's screen-share banner: measured off the frames, clear of the sheet
# tabs (which live at x < 330), so nothing the episode uses gets hidden.
DEFAULT_COVER = "730,986,460,44"


def die(msg: str) -> None:
    sys.exit(f"error: {msg}")


def ffmpeg() -> str:
    exe = shutil.which("ffmpeg")
    if not exe:
        die("ffmpeg not on PATH")
    return exe


def duration(path: Path) -> float:
    """Container duration, falling back to counting frames.

    Clipchamp's .webm exports often carry no duration in the header, which is
    why this cannot just read format=duration and trust it.
    """
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(path)], capture_output=True, text=True).stdout.strip()
    try:
        return float(out)
    except ValueError:
        pass
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-count_packets", "-select_streams", "v",
         "-show_entries", "stream=nb_read_packets,r_frame_rate", "-of", "json",
         str(path)], capture_output=True, text=True, check=True).stdout
    st = json.loads(out)["streams"][0]
    num, den = st["r_frame_rate"].split("/")
    return int(st["nb_read_packets"]) / (float(num) / float(den))


def read_srt(path: Path) -> list[tuple[float, float]]:
    text = path.read_text(encoding="utf-8-sig")
    cues = []
    for block in re.split(r"\n\s*\n", text.strip()):
        m = TIME.search(block)
        if not m:
            continue
        g = m.groups()
        to_s = lambda h, mi, s, ms: int(h) * 3600 + int(mi) * 60 + int(s) + int(ms) / 1000
        cues.append((to_s(*g[:4]), to_s(*g[4:])))
    if not cues:
        die(f"no cues found in {path.name}")
    return cues


def read_captions(path: Path) -> list[str]:
    """Caption lines: everything after the last `---` rule.

    An explicit marker rather than heuristics -- guessing which markdown lines
    are prose and which are notes is exactly the kind of thing that silently
    swallows a caption or adopts a sentence from the preamble.
    """
    text = path.read_text(encoding="utf-8")
    marker = chr(10) + "---"
    if marker not in text:
        die(f"{path.name} needs a '---' line; captions are the lines after it.")
    body = text.rsplit(marker, 1)[1]
    out = [l.strip() for l in body.splitlines() if l.strip()]
    if not out:
        die(f"{path.name} has no caption lines after the '---'")
    return out


async def measure(captions: list[str], voice: str, rate: int, tmp: Path) -> list[float]:
    """How long Andrew takes over each line. That sets the video's pace."""
    import edge_tts
    dur = []
    for i, text in enumerate(captions):
        if text in ("-", "x"):
            dur.append(0.0)
            continue
        text = text.lstrip(">").strip()      # outro lines are still spoken
        clip = tmp / f"m{i:02d}.mp3"
        sign = "+" if rate >= 0 else "-"
        await edge_tts.Communicate(text, voice, rate=f"{sign}{abs(rate)}%").save(str(clip))
        dur.append(duration(clip))
    return dur


def plan(cues, captions, spoken, total, gap_to, max_speed,
         gentle_first=0, gentle_speed=GENTLE_SPEED):
    """Build the segment list: alternating pauses and spoken stretches.

    Each segment records where it is in the source, how long it should become,
    and therefore how fast to play it. Speech that would need to exceed its cap
    is left longer instead -- extra air beats a frantic cursor.
    """
    segs, beats, outro = [], [], []
    cursor = 0.0
    spoken_index = 0
    for (start, end), text, want in zip(cues, captions, spoken):
        if text == "x":                 # cut entirely, along with its lead-in pause
            cursor = end
            continue
        if text.startswith(">"):        # cut from the picture, kept as an outro beat
            outro.append({"text": text.lstrip(">").strip(), "want": want})
            cursor = end
            continue
        if start > cursor + 0.04:                      # the pause before this line
            src = start - cursor
            segs.append({"a": cursor, "b": start, "target": min(src, gap_to),
                         "kind": "gap"})
        src = end - start
        if text == "-":
            segs.append({"a": start, "b": end, "target": min(src, gap_to), "kind": "gap"})
        else:
            # The opening gets a gentler cap than the body.
            cap = gentle_speed if spoken_index < gentle_first else max_speed
            spoken_index += 1
            target = max(want + SPEECH_PAD, src / cap)
            target = min(target, src)                  # never slow the picture down
            segs.append({"a": start, "b": end, "target": target, "kind": "speech",
                         "text": text})
        cursor = end
    if total > cursor + 0.04:
        segs.append({"a": cursor, "b": total, "target": min(total - cursor, gap_to),
                     "kind": "gap"})

    # Never hold on dead air before the recap card -- cut every trailing pause.
    while segs and segs[-1]["kind"] == "gap":
        segs.pop()

    clock = 0.0
    for seg in segs:
        src = seg["b"] - seg["a"]
        seg["speed"] = max(1.0, min(MAX_GAP_SPEED, src / seg["target"]))
        seg["out"] = src / seg["speed"]
        seg["at"] = clock
        if seg["kind"] == "speech":
            beats.append({"start": clock, "text": seg["text"]})
        clock += seg["out"]

    # Outro beats sit past the end of the picture. overlay_episode.py reads a
    # start time beyond the body as "this one belongs on the recap card".
    body = clock
    for i, line in enumerate(outro):
        beats.append({"start": clock + (0.3 if i else 0.2), "text": line["text"]})
        clock += line["want"] + (0.3 if i else 0.2)
    return segs, beats, body


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--video", required=True)
    ap.add_argument("--srt", required=True)
    ap.add_argument("--captions", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--voice", default=DEFAULT_VOICE)
    ap.add_argument("--rate", type=int, default=0)
    ap.add_argument("--gap", type=float, default=DEFAULT_GAP,
                    help=f"what a pause is squeezed to, seconds (default {DEFAULT_GAP})")
    ap.add_argument("--max-speed", type=float, default=MAX_SPEECH_SPEED,
                    help=f"fastest a spoken stretch may play (default {MAX_SPEECH_SPEED})")
    ap.add_argument("--gentle-first", type=int, default=GENTLE_FIRST,
                    help=f"spoken stretches at the start to cap at --gentle-speed "
                         f"(default {GENTLE_FIRST})")
    ap.add_argument("--gentle-speed", type=float, default=GENTLE_SPEED,
                    help=f"the opening's speed cap (default {GENTLE_SPEED})")
    ap.add_argument("--cover", default=DEFAULT_COVER,
                    help="x,y,w,h to paint white; 'none' to disable")
    args = ap.parse_args()

    ff = ffmpeg()
    video, srt = Path(args.video), Path(args.srt)
    for p in (video, srt, Path(args.captions)):
        if not p.exists():
            die(f"not found: {p}")

    cues = read_srt(srt)
    captions = read_captions(Path(args.captions))
    if len(cues) != len(captions):
        die(f"{len(cues)} cues in {srt.name} but {len(captions)} caption lines. "
            f"They must correspond one to one -- use '-' for a cue to drop.")
    total = duration(video)

    with tempfile.TemporaryDirectory() as td:
        print(f"measuring {sum(1 for c in captions if c not in ('-', 'x'))} "
              f"lines in {args.voice}")
        spoken = asyncio.run(measure(captions, args.voice, args.rate, Path(td)))
        segs, beats, out_len = plan(cues, captions, spoken, total,
                                    args.gap, args.max_speed,
                                    args.gentle_first, args.gentle_speed)

        outro_n = sum(1 for c in captions if c.startswith(">"))
        print(f"\n{total:.1f}s in -> {out_len:.1f}s out "
              f"({len(segs)} segments, {len(beats)} captions"
              + (f", {outro_n} over the recap card)" if outro_n else ")"))
        fast = [s for s in segs if s["kind"] == "speech" and s["speed"] > args.max_speed - 0.01]
        for seg in segs:
            if seg["kind"] != "speech":
                continue
            print(f"  {seg['at']:6.1f}s  x{seg['speed']:.2f}  "
                  f"{seg['b'] - seg['a']:4.1f}s -> {seg['out']:4.1f}s  {seg['text'][:52]}")
        if fast:
            print(f"\n{len(fast)} stretch(es) hit the {args.max_speed}x cap and stay "
                  f"longer than their line. Shorten those captions to tighten further.")

        # One filter graph: paint over the banner, split, retime each segment,
        # concat. Re-encoded once, so no generation loss beyond this pass.
        chain = []
        base = "0:v"
        if args.cover.lower() != "none":
            x, y, w, h = args.cover.split(",")
            chain.append(f"[0:v]drawbox=x={x}:y={y}:w={w}:h={h}:color=white@1:t=fill[cov]")
            base = "cov"
        chain.append(f"[{base}]split={len(segs)}" + "".join(f"[s{i}]" for i in range(len(segs))))
        for i, seg in enumerate(segs):
            chain.append(
                f"[s{i}]trim=start={seg['a']:.3f}:end={seg['b']:.3f},"
                f"setpts=(PTS-STARTPTS)/{seg['speed']:.5f},fps=30,"
                f"format=yuv420p,setsar=1[v{i}]")
        chain.append("".join(f"[v{i}]" for i in range(len(segs)))
                     + f"concat=n={len(segs)}:v=1:a=0[out]")

        out_path = Path(args.out)
        if not out_path.is_absolute():
            out_path = video.parent / out_path
        print("\nencoding...")
        subprocess.run(
            [ff, "-y", "-hide_banner", "-loglevel", "error", "-i", str(video),
             "-filter_complex", ";".join(chain), "-map", "[out]",
             "-c:v", "libx264", "-preset", "medium", "-crf", "20",
             "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(out_path)],
            check=True)

        beats_path = out_path.parent / "beats.md"
        body = ["# Caption beats", "",
                "Generated by `production/recut_from_srt.py`. Times are the RETIMED",
                f"recording's clock (`{out_path.name}`), where each spoken stretch was sped",
                "up to the length of Andrew's read of its caption.", "",
                f"Source: `{video.name}` + `{srt.name}`", "",
                "| Start | Text |", "| --- | --- |"]
        for beat in beats:
            tail = "  <!-- over the recap card -->" if beat["start"] >= out_len else ""
            body.append(f"| {beat['start']:.1f} | {beat['text']} |{tail}")
        beats_path.write_text("\n".join(body) + "\n", encoding="utf-8")

        actual = duration(out_path)
        print(f"wrote {out_path.name} ({out_path.stat().st_size / 1e6:.1f} MB, {actual:.1f}s)")
        print(f"wrote {beats_path.name} ({len(beats)} beats)")
        final = actual + 6.5
        # Josh, 2026-09-08: 2:00 plus or minus 30s is fine. 2:30 is the real edge.
        verdict = "fine" if final <= 150 else "TOO LONG"
        print(f"with cards: {final:.1f}s ({int(final // 60)}:{final % 60:04.1f}) -- {verdict}")


if __name__ == "__main__":
    main()
