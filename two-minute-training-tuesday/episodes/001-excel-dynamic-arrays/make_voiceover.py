"""Generate an AI voiceover for episode 001 and mux it onto the finished MP4.

Reads the beat-by-beat table out of narration.md -- which is itself generated
from the video's caption track -- so every line is placed at the picture's real
timecode instead of being nudged by hand on a timeline.

    pip install edge-tts
    python make_voiceover.py                      # Edge neural, default voice
    python make_voiceover.py --voice en-US-AriaNeural
    python make_voiceover.py --engine sapi --voice David     # offline preview
    python make_voiceover.py --list-voices

Two engines. `edge` is Microsoft's neural voices -- the same family Clipchamp
offers -- and needs network. `sapi` is the David/Zira voices already on every
Windows box: offline, instant, and audibly synthetic. Use sapi to hear the sync
and pacing in seconds, edge for anything you would actually publish.

Needs ffmpeg with libx264 on PATH (same requirement as render/make_video.py)
and outbound access to Microsoft's Edge TTS endpoint. Voices are the neural
ones Clipchamp offers; doing it here rather than in Clipchamp buys exact sync.

Any beat whose read runs longer than its window is re-synthesized faster, up to
--max-rate, and reported. If a beat still overruns it is left long and flagged --
better to hear it and rewrite the caption than to have it chipmunked.
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

HERE = Path(__file__).resolve().parent
NARRATION = HERE / "narration.md"
VIDEO_IN = HERE / "TMTT-001-Excel-Dynamic-Arrays.mp4"
VIDEO_OUT = HERE / "TMTT-001-Excel-Dynamic-Arrays-voiced.mp4"
AUDIO_OUT = HERE / "TMTT-001-narration.m4a"

DEFAULT_VOICE = "en-US-AndrewNeural"  # calm, mid-paced. Instruction, not marketing.
PAD = 0.15  # seconds of air to leave before the next beat starts
ROW = re.compile(r"^\|\s*([\d.]+)\s*\|\s*([\d.]+)s\s*\|\s*(\d+)\s*\|\s*(.+?)\s*\|$")


def ffmpeg() -> str:
    exe = shutil.which("ffmpeg")
    if not exe:
        sys.exit("ffmpeg not on PATH. See render/README.md -- needs libx264.")
    return exe


def beats() -> list[dict]:
    """The beat table from narration.md: start, window, and line."""
    rows = []
    for line in NARRATION.read_text(encoding="utf-8").splitlines():
        m = ROW.match(line.strip())
        if m:
            rows.append({"start": float(m.group(1)), "text": m.group(4)})
    if not rows:
        sys.exit(f"No beat table found in {NARRATION.name}.")
    total = duration(VIDEO_IN) if VIDEO_IN.exists() else rows[-1]["start"] + 6
    for i, b in enumerate(rows):
        nxt = rows[i + 1]["start"] if i + 1 < len(rows) else total
        b["budget"] = max(0.5, nxt - b["start"] - PAD)
    return rows


def duration(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "json", str(path)],
        capture_output=True, text=True, check=True,
    ).stdout
    return float(json.loads(out)["format"]["duration"])


SAPI_RATE_MAX = 10  # System.Speech uses -10..10, not a percentage


def say_sapi(text: str, out: Path, voice: str, rate: int) -> None:
    """David/Zira via System.Speech. Percent rate is mapped onto -10..10."""
    step = max(-SAPI_RATE_MAX, min(SAPI_RATE_MAX, round(rate / 10)))
    script = (
        "Add-Type -AssemblyName System.Speech; "
        "$s = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
        f"$s.SelectVoice('{voice}'); $s.Rate = {step}; "
        f"$s.SetOutputToWaveFile('{out}'); "
        f"$s.Speak([System.IO.File]::ReadAllText('{out.with_suffix('.txt')}')); "
        "$s.Dispose()"
    )
    out.with_suffix(".txt").write_text(text, encoding="utf-8")
    subprocess.run(["powershell", "-NoProfile", "-Command", script],
                   check=True, capture_output=True)


def sapi_voice_name(want: str) -> str:
    """Accept 'David' or the full 'Microsoft David Desktop'."""
    out = subprocess.run(
        ["powershell", "-NoProfile", "-Command",
         "Add-Type -AssemblyName System.Speech; "
         "(New-Object System.Speech.Synthesis.SpeechSynthesizer)"
         ".GetInstalledVoices().VoiceInfo.Name"],
        capture_output=True, text=True, check=True).stdout.splitlines()
    names = [n.strip() for n in out if n.strip()]
    for n in names:
        if want.lower() in n.lower():
            return n
    sys.exit(f"No SAPI voice matching {want!r}. Installed: {', '.join(names)}")


async def say(text: str, out: Path, voice: str, rate: int) -> None:
    import edge_tts
    sign = "+" if rate >= 0 else "-"
    tts = edge_tts.Communicate(text, voice, rate=f"{sign}{abs(rate)}%")
    await tts.save(str(out))


async def synth(rows: list[dict], voice: str, base: int, max_rate: int,
                tmp: Path, engine: str):
    """One clip per beat, sped up only as far as its window demands."""
    ext = "wav" if engine == "sapi" else "mp3"

    async def render(text: str, clip: Path, rate: int) -> float:
        if engine == "sapi":
            say_sapi(text, clip, voice, rate)
        else:
            await say(text, clip, voice, rate)
        return duration(clip)

    long = []
    for i, b in enumerate(rows, 1):
        clip = tmp / f"beat{i:02d}.{ext}"
        rate = base
        d = await render(b["text"], clip, rate)
        while d > b["budget"] and rate < max_rate:
            rate = min(max_rate, rate + max(4, int(100 * (d / b["budget"] - 1))))
            d = await render(b["text"], clip, rate)
        b.update(clip=clip, dur=d, rate=rate)
        flag = ""
        if d > b["budget"]:
            flag = f"  OVERRUNS by {d - b['budget']:.1f}s"
            long.append(b)
        print(f"  {i:2d}. {b['start']:6.1f}s  {d:4.1f}s / {b['budget']:4.1f}s"
              f"  rate {rate:+3d}%{flag}")
    return long


def mix(rows: list[dict], out: Path, ff: str, total: float) -> None:
    """Delay each clip to its timecode and sum them into one track.

    The track is padded out to the picture's full length. The last word lands
    before the recap card does, and without the pad ffmpeg's -shortest would
    trim the video down to the audio and cut the recap frame off.
    """
    cmd = [ff, "-y", "-v", "error"]
    for b in rows:
        cmd += ["-i", str(b["clip"])]
    parts = [f"[{i}:a]adelay={int(b['start'] * 1000)}|{int(b['start'] * 1000)}[a{i}]"
             for i, b in enumerate(rows)]
    chain = ";".join(parts) + ";"
    chain += "".join(f"[a{i}]" for i in range(len(rows)))
    chain += (f"amix=inputs={len(rows)}:normalize=0:dropout_transition=0,"
              f"apad,atrim=0:{total:.3f}[mix]")
    cmd += ["-filter_complex", chain, "-map", "[mix]",
            "-c:a", "aac", "-b:a", "160k", str(out)]
    subprocess.run(cmd, check=True)


def mux(video: Path, audio: Path, out: Path, ff: str) -> None:
    """Picture is copied, not re-encoded -- no second generation loss."""
    subprocess.run(
        [ff, "-y", "-v", "error", "-i", str(video), "-i", str(audio),
         "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac",
         str(out)],
        check=True,
    )


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--engine", choices=("edge", "sapi"), default="edge",
                    help="edge = neural, needs network; sapi = offline David/Zira")
    ap.add_argument("--voice", default=None,
                    help=f"default {DEFAULT_VOICE} for edge, David for sapi")
    ap.add_argument("--rate", type=int, default=0,
                    help="base speed adjustment, percent (default 0)")
    ap.add_argument("--max-rate", type=int, default=20,
                    help="ceiling when a beat has to be sped up to fit")
    ap.add_argument("--list-voices", action="store_true")
    ap.add_argument("--keep-audio", action="store_true",
                    help="also write the bare narration track")
    args = ap.parse_args()

    if args.list_voices and args.engine == "sapi":
        print(subprocess.run(
            ["powershell", "-NoProfile", "-Command",
             "Add-Type -AssemblyName System.Speech; "
             "(New-Object System.Speech.Synthesis.SpeechSynthesizer)"
             ".GetInstalledVoices().VoiceInfo.Name"],
            capture_output=True, text=True, check=True).stdout.strip())
        return

    if args.list_voices:
        import edge_tts

        async def show():
            mgr = await edge_tts.VoicesManager.create()
            for v in mgr.find(Language="en"):
                print(f"{v['ShortName']:34s} {v['Gender']:6s} {v['Locale']}")
        asyncio.run(show())
        return

    ff = ffmpeg()
    if not VIDEO_IN.exists():
        sys.exit(f"{VIDEO_IN.name} not found. Render it first: render/make_video.py")

    voice = args.voice or (DEFAULT_VOICE if args.engine == "edge" else "David")
    if args.engine == "sapi":
        voice = sapi_voice_name(voice)

    rows = beats()
    print(f"{len(rows)} beats from {NARRATION.name}, {args.engine} voice {voice}")
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        long = asyncio.run(
            synth(rows, voice, args.rate, args.max_rate, tmp, args.engine))
        track = tmp / "narration.m4a"
        mix(rows, track, ff, duration(VIDEO_IN))
        slug = voice.replace("Microsoft ", "").replace(" Desktop", "")
        slug = slug.replace("Neural", "").replace("en-US-", "").replace(" ", "")
        out_video = VIDEO_OUT.with_name(
            f"{VIDEO_OUT.stem}-{slug.lower()}{VIDEO_OUT.suffix}")
        mux(VIDEO_IN, track, out_video, ff)
        if args.keep_audio:
            shutil.copy(track, AUDIO_OUT)
            print(f"wrote {AUDIO_OUT.name}")

    size = out_video.stat().st_size / 1e6
    print(f"wrote {out_video.name} ({size:.1f} MB, {duration(out_video):.1f}s)")
    if long:
        print(f"\n{len(long)} beat(s) still overrun their window even at "
              f"{args.max_rate:+d}%. Shorten the caption in render/episode.html, "
              f"re-run make_narration.py, and re-render:")
        for b in long:
            print(f"  {b['start']:.1f}s  {b['text']}")


if __name__ == "__main__":
    main()
