"""Turn raw window grabs into clean 1920x1080 episode frames.

Every rule in here exists because something reached a finished render without it. Read the
comments before changing any constant.

    python prepare_frames.py --in frames/raw --out frames/clean
    python prepare_frames.py --in frames/raw --out frames/clean --modal s06 s07 s08

What it does, in order:

1. **Crops Chrome's "started debugging this browser" infobar, if present.** The bar appears
   whenever the automation reconnects -- which is after essentially every action -- so it
   cannot be dismissed once and forgotten. The rows it occupies are replaced with the color
   of the page's own header band, which is flat, so the join is invisible. A fixed crop
   calibrated on one frame is NOT enough: the first 003 cut checked a single frame, that frame
   happened to be the only clean one, and the banner shipped in twelve others.

2. **Paints out Outlook's next-meeting reminder**, top right, which otherwise carries a real
   meeting title into every frame.

3. **Masks the strip of live mail beside a settings dialog**, for frames named with --modal.
   The modal does not cover the window; on 003 that strip carried truncated subject lines and
   an invoice number. This belongs here rather than in a post-pass: a mask painted on the
   frames afterwards is silently undone the next time they are regenerated, which is exactly
   what happened, and the leak came back to a render that had already been "fixed".

4. **Pads to 1080 rather than upscaling** when the page is short, using the colors of its own
   top and bottom rows. Rescaling screen text is the fault these episodes exist to avoid.

None of this replaces reading the finished video. See recording-setup.md.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw

W, H = 1920, 1080

# Measured against new Outlook in Chrome at 1920x1080, 2026-09. Re-measure if the chrome
# changes; a wrong constant here is invisible until you look at a frame.
REMINDER = (1600, 24, 1920, 132)     # next-meeting widget, relative to the page top.
                                     # Deliberately generous: the widget shifts with the
                                     # list layout, and a box that just misses it looks
                                     # exactly like a box that worked.
MODAL_STRIP = (1598, 300, 1920, 1080)  # live mail visible past the settings dialog


def banner_bottom(im: Image.Image) -> int:
    """Last row of Chrome's infobar, or 0 when it is not showing.

    Identified by its blue "Cancel" pill *together with* the pale band either side. Requiring
    both matters: the pill alone matches blue buttons inside the page, which made an earlier
    version crop 50 rows off perfectly good frames.
    """
    px = im.load()
    rows = []
    for y in range(0, min(320, im.height)):
        pill = any(px[x, y][2] > 175 and px[x, y][0] < 120 and px[x, y][1] < 150
                   for x in range(1000, min(1200, im.width), 4))
        band = all(min(px[x, y]) > 230 for x in range(300, min(900, im.width), 50))
        if pill and band:
            rows.append(y)
    return max(rows) + 10 if rows else 0


def prepare(src: Path, dst: Path, modal: bool = False, page_top: int = 0) -> dict:
    im = Image.open(src).convert("RGB")
    if page_top:
        # Windowed capture: cut the browser's own chrome (tabs, address bar,
        # bookmarks) so the frame is pure app. Fullscreen capture needs page_top=0.
        im = im.crop((8, page_top, min(8 + W, im.width), im.height))
    note = {"src": src.name, "banner": 0, "padded": 0, "modal": modal}

    top = banner_bottom(im)
    if top:
        note["banner"] = top
        body = im.crop((0, top, im.width, im.height))
        im = Image.new("RGB", (body.width, body.height + top))
        im.paste(Image.new("RGB", (body.width, top), body.getpixel((300, 25))), (0, 0))
        im.paste(body, (0, top))

    if im.width != W:
        im = im.crop((0, 0, W, im.height)) if im.width > W else im

    if im.height > H:
        im = im.crop((0, 0, W, H))
    elif im.height < H:
        pad = H - im.height
        up, down = pad // 2, pad - pad // 2
        note["padded"] = pad
        out = Image.new("RGB", (W, H))
        out.paste(im.crop((0, 0, W, 1)).resize((W, up)), (0, 0))
        out.paste(im, (0, up))
        out.paste(im.crop((0, im.height - 1, W, im.height)).resize((W, down)), (0, up + im.height))
        im = out

    d = ImageDraw.Draw(im)
    d.rectangle(REMINDER, fill=im.getpixel((REMINDER[0] - 40, REMINDER[1] + 4)))
    if modal:
        d.rectangle(MODAL_STRIP, fill=im.getpixel((MODAL_STRIP[2] - 40, MODAL_STRIP[3] - 40)))

    dst.parent.mkdir(parents=True, exist_ok=True)
    im.save(dst)
    return note


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--in", dest="src", required=True, help="directory of raw window grabs")
    ap.add_argument("--out", dest="dst", required=True, help="directory for prepared frames")
    ap.add_argument("--page-top", type=int, default=0, dest="page_top",
                    help="row where the app's own UI starts in a WINDOWED capture, i.e. below "
                         "the browser chrome. 0 for a fullscreen capture, which has none.")
    ap.add_argument("--modal", nargs="*", default=[],
                    help="name prefixes of frames where a settings dialog is open, so the "
                         "strip of live mail beside it is masked")
    args = ap.parse_args()

    src = Path(args.src)
    files = sorted(src.glob("*.png"))
    if not files:
        sys.exit(f"no PNGs in {src}")

    for f in files:
        modal = any(f.stem.startswith(m) for m in args.modal)
        n = prepare(f, Path(args.dst) / f.name, modal, args.page_top)
        bits = []
        if n["banner"]:
            bits.append(f"banner {n['banner']}px")
        if n["padded"]:
            bits.append(f"padded {n['padded']}px")
        if n["modal"]:
            bits.append("modal masked")
        print(f"{f.name:28} {', '.join(bits) or 'clean'}")

    print(f"\n{len(files)} frames -> {args.dst}")
    print("Now LOOK at them. Read the From and Subject columns, and the edges of every dialog.")


if __name__ == "__main__":
    main()
