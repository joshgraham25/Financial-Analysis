#!/usr/bin/env python3
"""Copy this repo's episodes.json into the Desktop Hub, which reads its own copy.

    python3 distribution/sync_hub_manifest.py            # check only
    python3 distribution/sync_hub_manifest.py --write

The Hub's TrainingSeriesOptions is explicit that its manifest is a COPY and this
repo is the source of truth -- but nothing enforced it, and by 2026-09-25 the two
had drifted badly: the Hub still called the series "Two-Minute Training Tuesday"
months after the rename, and showed episode 002 with no videoUrl, so the Watch
button was missing for an episode that had been published for two weeks. Nobody
noticed because the Hub section and the email job are looked at by different
people on different days.

Run this whenever an episode publishes or the catalogue changes, and commit BOTH
repos. The Hub re-reads the file on a timestamp check (60s) rather than at
startup, so the live section updates without a restart -- but a later deploy
overwrites it from the Hub repo, so the Hub's copy must be committed too or the
change silently reverts on the next unrelated deploy.
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent / "episodes.json"
DST = (Path(__file__).resolve().parents[3] / "clc-hub" /
       "src" / "Clc.DesktopHub.Api" / "data" / "training-series.json")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--write", action="store_true", help="actually copy; default is a dry check")
    ap.add_argument("--dst", default=None, help="override the Hub manifest path")
    args = ap.parse_args()

    dst = Path(args.dst) if args.dst else DST
    if not SRC.exists():
        sys.exit(f"no source manifest at {SRC}")
    if not dst.exists():
        sys.exit(f"no Hub manifest at {dst} -- pass --dst if the Hub lives elsewhere")

    src_text = SRC.read_text(encoding="utf-8")
    if dst.read_text(encoding="utf-8") == src_text:
        print("in sync")
        return

    a, b = json.loads(dst.read_text(encoding="utf-8")), json.loads(src_text)
    if a["series"]["name"] != b["series"]["name"]:
        print(f"  series name : {a['series']['name']!r} -> {b['series']['name']!r}")
    have = {e["number"]: e for e in a["episodes"]}
    for e in b["episodes"]:
        old = have.get(e["number"])
        if old is None:
            print(f"  + episode {e['number']:03d}  {e['title']}")
            continue
        for k in ("title", "runtime", "published", "videoUrl"):
            if old.get(k) != e.get(k):
                o, n = old.get(k), e.get(k)
                if k == "videoUrl":
                    o, n = ("set" if o else "empty"), ("set" if n else "empty")
                print(f"  ~ episode {e['number']:03d}  {k}: {o!r} -> {n!r}")

    if not args.write:
        print("\ndry run -- pass --write to apply, then commit BOTH repos")
        return
    dst.write_text(src_text, encoding="utf-8")
    print(f"\nwrote {dst}")


if __name__ == "__main__":
    main()
