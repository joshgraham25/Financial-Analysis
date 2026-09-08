"""Overlay Two-Minute Training Tuesday branding onto a real screen recording.

This is the pipeline for every episode from 002 onward. Josh records real Excel
(or Outlook, or whatever the tip is about); this script adds the title card, the
burnt-in captions, the recap card, and optionally the AI voiceover -- so the
picture is genuinely the application and only the wrapper is generated.

It replaces the synthetic renderer for good reason: a drawn Excel is a drawing
of Excel. Rule 0 in style-guide.md asks for one hundred percent fidelity, and a
recording is the only thing that gets there.

    pip install pillow
    pip install pillow edge-tts
    python overlay_episode.py --episode 002 --video raw-recording.mp4 --check
    python overlay_episode.py --episode 002 --video raw-recording.mp4
    python overlay_episode.py --episode 002 --video raw.mp4 --silent   # no voiceover

The voiceover is on by default and speaks the beats table in Andrew's voice
(Josh's choice, 2026-09-08 -- consistent week to week, and it means a line can be
re-cut without re-recording the screen). Each beat is synthesized separately and
delayed to its own timecode, so the words land on the action rather than being
nudged along a timeline by hand. A beat whose read overruns its window is
re-synthesized faster, up to --max-rate, and reported if it still does not fit --
better to hear it and shorten the caption than to chipmunk it.

Inputs
------
--video   The raw recording. Any size; it is scaled and padded to 1920x1080.
--beats   The caption/narration table. Defaults to the episode's beats.md.
          Markdown, one row per beat, and the times are the RECORDING's own
          clock -- not the old synthetic script's:

              | Start | Text |
              | ---   | ---  |
              | 0.0   | Welcome to Two-Minute Training Tuesday. |
              | 4.2   | Last week this drop-down changed the whole report. |

          Each caption runs until the next beat starts, less a small gap.

--check   Write the cards and a few overlaid stills as PNGs and stop. Always run
          this first: it costs seconds and shows whether the beats line up with
          what is actually on screen. No audio is synthesized in check mode.

--silent  Skip the voiceover. Use it when Josh narrated into the recording, or
          for a clean picture to voice elsewhere.

Output    <episode folder>/TMTT-<nnn>-<slug>-overlay.mp4

Needs ffmpeg with libx264 on PATH, and outbound access to Microsoft's Edge TTS
endpoint for the voiceover.
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

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
EPISODES = ROOT / "episodes"
BRAND_JSON = ROOT / "brand.json"
CATALOGUE = ROOT / "episodes.json"

W, H = 1920, 1080
FPS = 30
SERIES = "Two-Minute Training Tuesday"

TITLE_CARD_S = 2.5
RECAP_CARD_S = 4.0
CAPTION_GAP = 0.15          # air between one caption and the next
CAPTION_MIN = 1.2

# Josh's voice choice for the series, 2026-09-08. Calm, mid-paced: instruction,
# not marketing. Keep it stable -- a changing narrator reads as a different show.
DEFAULT_VOICE = "en-US-AndrewNeural"
VOICE_PAD = 0.15            # air to leave before the next beat's line starts

FONTS = Path("C:/Windows/Fonts")
F_REG, F_SEMI, F_BOLD = "segoeui.ttf", "seguisb.ttf", "segoeuib.ttf"

BEAT_ROW = re.compile(r"^\|\s*([\d.]+)\s*\|\s*(.+?)\s*\|$")


def die(msg: str) -> None:
    sys.exit(f"error: {msg}")


def ffmpeg() -> str:
    exe = shutil.which("ffmpeg")
    if not exe:
        die("ffmpeg not on PATH. See episodes/001-.../render/README.md -- needs libx264.")
    return exe


def probe_duration(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(path)],
        capture_output=True, text=True, check=True).stdout
    return float(json.loads(out)["format"]["duration"])


def brand() -> dict:
    base = {"dark": "#15171c", "accent": "#e0303e", "header": "#a8121f",
            "tint": "#fdecee", "input": "#fff0dc", "muted": "#c6cbd6"}
    if BRAND_JSON.exists():
        raw = json.loads(BRAND_JSON.read_text(encoding="utf-8"))
        base.update({k: v for k, v in raw.items() if not k.startswith("_")})
    return base


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONTS / name), size)


def episode_meta(number: int) -> dict:
    """Title and recap lines come from the catalogue, so they are written once."""
    if not CATALOGUE.exists():
        die(f"{CATALOGUE.name} not found")
    data = json.loads(CATALOGUE.read_text(encoding="utf-8"))
    for ep in data.get("episodes", data if isinstance(data, list) else []):
        if ep.get("number") == number:
            return ep
    die(f"episode {number:03d} is not in {CATALOGUE.name}")


def episode_dir(meta: dict) -> Path:
    d = EPISODES / meta["slug"]
    if not d.is_dir():
        die(f"{d} does not exist")
    return d


def read_beats(path: Path) -> list[dict]:
    if not path.exists():
        die(f"no beats file at {path}. Write one -- see this script's docstring.")
    beats = []
    for line in path.read_text(encoding="utf-8").splitlines():
        # Strip trailing HTML comments first. recut_from_srt.py annotates the
        # outro rows with one, and matching the row pattern against it silently
        # dropped exactly those beats -- the ones that matter least often and
        # are hardest to notice missing.
        line = re.sub(r"<!--.*?-->", "", line).strip()
        m = BEAT_ROW.match(line.strip())
        if not m:
            continue
        text = m.group(2).strip()
        if text.lower() in {"text", "caption"} or set(text) <= set("- "):
            continue                     # header and divider rows
        beats.append({"start": float(m.group(1)), "text": text})
    if not beats:
        die(f"{path.name} has no beat rows. Expected '| 4.2 | Some caption. |'")
    beats.sort(key=lambda b: b["start"])
    return beats


def wrap(draw, text: str, fnt, max_w: int) -> list[str]:
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def caption_png(text: str, out: Path, b: dict) -> None:
    """A transparent frame carrying just the caption bar, ready to overlay."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    fnt = font(F_BOLD, 44)
    lines = wrap(draw, text, fnt, int(W * 0.72))
    line_h = 56
    pad_x, pad_y = 46, 26
    box_w = max(draw.textlength(l, font=fnt) for l in lines) + pad_x * 2
    box_h = line_h * len(lines) + pad_y * 2
    x0 = (W - box_w) / 2
    y0 = H - 118 - box_h
    draw.rounded_rectangle([x0, y0, x0 + box_w, y0 + box_h], radius=16,
                           fill=(*hex_rgb(b["dark"]), 235))
    for i, line in enumerate(lines):
        lw = draw.textlength(line, font=fnt)
        draw.text(((W - lw) / 2, y0 + pad_y + i * line_h), line, font=fnt, fill="#ffffff")
    img.save(out)


def hex_rgb(value: str) -> tuple[int, int, int]:
    v = value.lstrip("#")
    return tuple(int(v[i:i + 2], 16) for i in (0, 2, 4))


def title_png(meta: dict, out: Path, b: dict) -> None:
    img = Image.new("RGB", (W, H), b["dark"])
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, 14, H], fill=b["accent"])
    draw.text((150, 300), SERIES.upper(), font=font(F_SEMI, 40), fill=b["accent"])
    draw.text((150, 372), f"Episode {meta['number']:03d}", font=font(F_REG, 36),
              fill=b["muted"])
    fnt = font(F_BOLD, 92)
    for i, line in enumerate(wrap(draw, meta["title"], fnt, W - 300)):
        draw.text((150, 470 + i * 112), line, font=fnt, fill="#ffffff")
    img.save(out)


def recap_png(meta: dict, out: Path, b: dict) -> None:
    img = Image.new("RGB", (W, H), b["dark"])
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, 14, H], fill=b["accent"])
    draw.text((150, 220), "RECAP", font=font(F_SEMI, 40), fill=b["accent"])
    fnt_t = font(F_BOLD, 66)
    y = 300
    for line in wrap(draw, meta["title"], fnt_t, W - 300):
        draw.text((150, y), line, font=fnt_t, fill="#ffffff")
        y += 82
    y += 40
    fnt_r = font(F_REG, 48)
    for i, line in enumerate(meta.get("recap", []), 1):
        draw.text((150, y), f"{i}.", font=font(F_SEMI, 48), fill=b["accent"])
        draw.text((225, y), line, font=fnt_r, fill="#ffffff")
        y += 78
    img.save(out)


async def say(text: str, out: Path, voice: str, rate: int) -> None:
    import edge_tts
    sign = "+" if rate >= 0 else "-"
    await edge_tts.Communicate(text, voice, rate=f"{sign}{abs(rate)}%").save(str(out))


async def synth(beats: list[dict], voice: str, base: int, max_rate: int,
                tmp: Path) -> list[dict]:
    """One clip per beat, sped up only as far as its own window demands."""
    long = []
    for i, beat in enumerate(beats, 1):
        clip = tmp / f"beat{i:02d}.mp3"
        budget = max(0.5, beat["end"] - beat["start"] - VOICE_PAD)
        rate = base
        await say(beat["text"], clip, voice, rate)
        d = probe_duration(clip)
        while d > budget and rate < max_rate:
            rate = min(max_rate, rate + max(4, int(100 * (d / budget - 1))))
            await say(beat["text"], clip, voice, rate)
            d = probe_duration(clip)
        beat["clip"] = clip
        flag = ""
        if d > budget:
            flag = f"  OVERRUNS by {d - budget:.1f}s"
            long.append(beat)
        print(f"  {i:2d}. {beat['start']:6.1f}s  {d:4.1f}s / {budget:4.1f}s"
              f"  rate {rate:+3d}%{flag}")
    return long


def build(args) -> None:
    ff = ffmpeg()
    b = brand()
    meta = episode_meta(args.episode)
    folder = episode_dir(meta)
    video = Path(args.video)
    if not video.is_absolute():
        video = (folder / video) if (folder / video).exists() else video
    if not video.exists():
        die(f"recording not found: {video}")

    beats_path = Path(args.beats) if args.beats else folder / "beats.md"
    beats = read_beats(beats_path)
    body = probe_duration(video)

    # Each caption runs to the next beat, so the table needs no end times.
    for i, beat in enumerate(beats):
        nxt = beats[i + 1]["start"] if i + 1 < len(beats) else None
        if nxt is not None:
            limit = nxt - CAPTION_GAP
        else:
            # The last beat has no successor to run up to, and it is what sizes
            # the recap card. Estimate from the line's own length -- a fixed
            # fallback here inflated the card to a full minute.
            limit = beat["start"] + len(beat["text"].split()) * 0.36 + 0.8
        beat["end"] = max(beat["start"] + CAPTION_MIN, limit)

    # A beat starting past the end of the picture belongs on the recap card,
    # which grows to hold it. This is how the outro plays over the card.
    over_card = [x for x in beats if x["start"] >= body]
    recap_s = RECAP_CARD_S
    if over_card:
        recap_s = max(RECAP_CARD_S, max(x["end"] for x in over_card) - body + 0.6)
        print(f"{len(over_card)} beat(s) play over the recap card, "
              f"which runs {recap_s:.1f}s")
    for beat in beats:
        beat["end"] = min(beat["end"], body + recap_s)

    workdir = Path(tempfile.mkdtemp(prefix="tmtt-overlay-"))
    try:
        title = workdir / "title.png"
        recap = workdir / "recap.png"
        title_png(meta, title, b)
        recap_png(meta, recap, b)
        for i, beat in enumerate(beats):
            beat["png"] = workdir / f"cap{i:02d}.png"
            caption_png(beat["text"], beat["png"], b)

        if args.check:
            out = folder / "overlay-check"
            out.mkdir(exist_ok=True)
            shutil.copy(title, out / "title-card.png")
            shutil.copy(recap, out / "recap-card.png")
            # A still from the middle of each of the first few captions, so the
            # beat times can be checked against what is really on screen.
            for beat in beats[:6]:
                at = (beat["start"] + beat["end"]) / 2
                still = out / f"at-{at:06.2f}.png"
                subprocess.run(
                    [ff, "-y", "-v", "error", "-ss", f"{at:.2f}", "-i", str(video),
                     "-i", str(beat["png"]), "-filter_complex",
                     f"[0:v]scale={W}:{H}:force_original_aspect_ratio=decrease,"
                     f"pad={W}:{H}:(ow-iw)/2:(oh-ih)/2:color=black[v];[v][1:v]overlay=0:0",
                     "-frames:v", "1", str(still)], check=True)
                print("wrote", still)
            print(f"\n{len(beats)} beats, recording {body:.1f}s, "
                  f"final {body + TITLE_CARD_S + recap_s:.1f}s")
            print(f"cards + stills in {out}")
            return

        # One pass: normalise the picture, burn every caption, then bracket the
        # result with the two cards. Cards are concatenated rather than overlaid
        # so they are genuinely full frames.
        cmd = [ff, "-y", "-hide_banner", "-loglevel", "error",
               "-loop", "1", "-t", str(TITLE_CARD_S), "-i", str(title),
               "-i", str(video),
               "-loop", "1", "-t", str(recap_s), "-i", str(recap)]
        for beat in beats:
            cmd += ["-i", str(beat["png"])]

        # Cards first, captions second. Burning captions into the body alone --
        # which is what this did originally -- makes an outro over the recap card
        # impossible to express, because the caption has nowhere to live.
        chain = [
            f"[1:v]scale={W}:{H}:force_original_aspect_ratio=decrease,"
            f"pad={W}:{H}:(ow-iw)/2:(oh-ih)/2:color=black,fps={FPS},"
            f"format=yuv420p,setsar=1[mid]"
        ]
        for idx, name in ((0, "pre"), (2, "post")):
            chain.append(f"[{idx}:v]scale={W}:{H},fps={FPS},format=yuv420p,setsar=1[{name}]")
        chain.append("[pre][mid][post]concat=n=3:v=1:a=0[cat0]")
        cur = "cat0"
        for i, beat in enumerate(beats):
            nxt = f"cat{i + 1}"
            # Beat times are the picture's clock; the title card shifts them.
            a = TITLE_CARD_S + beat["start"]
            b = TITLE_CARD_S + beat["end"]
            chain.append(
                f"[{cur}][{i + 3}:v]overlay=0:0:"
                f"enable='between(t,{a:.3f},{b:.3f})'[{nxt}]")
            cur = nxt
        chain.append(f"[{cur}]null[out]")

        out_path = folder / f"TMTT-{meta['number']:03d}-{slug(meta)}.mp4"
        total = TITLE_CARD_S + body + recap_s

        # Audio, in order of preference: the generated voiceover, else whatever
        # the recording itself carries. Either way it is delayed past the title
        # card -- otherwise every word lands 2.5s early -- and padded to the full
        # length, or ffmpeg trims the picture down to the audio and eats the
        # recap card.
        audio_out = None
        if args.voice:
            print(f"{len(beats)} beats, {args.voice}")
            long = asyncio.run(
                synth(beats, args.voice, args.rate, args.max_rate, workdir))
            first = len(beats) + 3          # cards + video + caption PNGs
            for beat in beats:
                cmd += ["-i", str(beat["clip"])]
            parts = []
            for i, beat in enumerate(beats):
                ms = int((TITLE_CARD_S + beat["start"]) * 1000)
                parts.append(f"[{first + i}:a]adelay={ms}|{ms}[va{i}]")
            chain += parts
            chain.append(
                "".join(f"[va{i}]" for i in range(len(beats)))
                + f"amix=inputs={len(beats)}:normalize=0:dropout_transition=0,"
                  f"apad,atrim=0:{total:.3f}[aout]")
            audio_out = "[aout]"
        elif has_audio(video):
            delay = int(TITLE_CARD_S * 1000)
            chain.append(f"[1:a]adelay={delay}|{delay},apad,atrim=0:{total:.3f}[aout]")
            audio_out = "[aout]"
            long = []
        else:
            long = []

        cmd += ["-filter_complex", ";".join(chain), "-map", "[out]"]
        if audio_out:
            cmd += ["-map", audio_out, "-c:a", "aac", "-b:a", "160k"]
        cmd += ["-c:v", "libx264", "-preset", "slow", "-crf", "20",
                "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(out_path)]
        print(f"{len(beats)} captions onto {body:.1f}s of recording")
        subprocess.run(cmd, check=True)
        actual = probe_duration(out_path)
        print(f"wrote {out_path.name} ({out_path.stat().st_size / 1e6:.1f} MB, {actual:.1f}s)")
        if actual > 120:
            print(f"WARNING: {actual:.1f}s is over the 2:00 ceiling in style-guide.md")
        if long:
            print(f"\n{len(long)} beat(s) still overrun their window at "
                  f"{args.max_rate:+d}%. Shorten the caption in beats.md and re-run:")
            for beat in long:
                print(f"  {beat['start']:.1f}s  {beat['text']}")
    finally:
        shutil.rmtree(workdir, ignore_errors=True)


def has_audio(path: Path) -> bool:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries",
         "stream=index", "-of", "json", str(path)],
        capture_output=True, text=True, check=True).stdout
    return bool(json.loads(out).get("streams"))


def slug(meta: dict) -> str:
    """A short, stable name from the episode's folder slug.

    Built from the title, this produced
    'Data-Validation-the-basic-way-and-the-way-that-m' -- truncated mid-word,
    and it would change if the title were ever reworded. The folder slug is
    short and already stable.
    """
    stem = re.sub(r"^\d+-", "", meta["slug"])
    return "-".join(w.capitalize() for w in stem.split("-"))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--episode", type=int, required=True, help="episode number, e.g. 2")
    ap.add_argument("--video", required=True, help="the raw screen recording")
    ap.add_argument("--beats", default=None, help="beats table (default: <episode>/beats.md)")
    ap.add_argument("--check", action="store_true",
                    help="write the cards and a few overlaid stills, then stop")
    ap.add_argument("--voice", default=DEFAULT_VOICE,
                    help=f"Edge neural voice (default {DEFAULT_VOICE})")
    ap.add_argument("--silent", action="store_true",
                    help="no voiceover -- keeps the recording's own audio if it has any")
    ap.add_argument("--rate", type=int, default=0,
                    help="base speed adjustment, percent (default 0)")
    ap.add_argument("--max-rate", type=int, default=20,
                    help="ceiling when a beat has to be sped up to fit its window")
    args = ap.parse_args()
    if args.silent:
        args.voice = None
    build(args)


if __name__ == "__main__":
    main()
