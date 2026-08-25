#!/usr/bin/env python3
"""Compose and send the weekly Two-Minute Training Tuesday email.

Reads the episode catalogue, renders the message, and sends it. Intended to run
ON the Thomas Anderson host with the shared SMTP config sourced, so no host name
or credential is ever handled off-host:

    . ~/.config/clc-shared/smtp.env.sh
    python3 send_episode_email.py --episode 1 --to someone@creativeliquidcoatings.com

Refuses to send an episode with no videoUrl. A weekly email whose link 404s is
worse than no email -- it teaches people the series is broken.

--dry-run writes the HTML to stdout and sends nothing. That is how you review a
draft; there is deliberately no "send to everyone" default and no recipient list
baked in, because an address list in a script rots and keeps mailing leavers.

This is the standalone version, used to validate the layout and deliverability
before the same composition moves into the Hub as a hosted service (the Worker
project is never deployed -- deploy.sh publishes Api only).
"""

from __future__ import annotations

import argparse
import json
import os
import smtplib
import sys
from email.message import EmailMessage
from email.utils import formataddr
from pathlib import Path

# CLC palette, from clc-theme.css. Inline only -- Outlook drops <style> blocks.
RED = "#a8121f"
RED_BRIGHT = "#ce1f2d"
CHARCOAL = "#15171c"
INK = "#15171c"
INK_MUTED = "#5b6270"
LINE = "#d5dae2"
TINT = "#fdecee"
PAPER = "#e9ecf1"


def load_manifest(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def find_episode(manifest: dict, number: int) -> dict:
    for episode in manifest["episodes"]:
        if episode["number"] == number:
            return episode
    sys.exit(f"No episode {number} in the manifest.")


def render_html(series: dict, ep: dict, recap: list[str]) -> str:
    """Table-based, inline-styled, single column. Outlook renders no flexbox and
    no grid, and strips <style>; anything cleverer than this breaks in the client
    most of the company reads mail in."""
    number = f"{ep['number']:03d}"
    library = series.get("sharePoint", {}).get("folderUrl", "")

    recap_rows = "".join(
        f"""
        <tr><td style="padding:4px 0;font:14px/1.5 Consolas,'Courier New',monospace;color:{INK};">
          {item}
        </td></tr>"""
        for item in recap
    )

    library_line = (
        f"""<p style="margin:22px 0 0;font:13px/1.6 'Segoe UI',Arial,sans-serif;color:{INK_MUTED};">
             Every episode lives in
             <a href="{library}" style="color:{RED};">the Two-Minute Training Tuesday library</a>.
           </p>"""
        if library
        else ""
    )

    return f"""<!doctype html>
<html><body style="margin:0;padding:0;background:{PAPER};">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0"
       style="background:{PAPER};padding:24px 12px;">
 <tr><td align="center">
  <table role="presentation" width="600" cellpadding="0" cellspacing="0"
         style="width:600px;max-width:100%;background:#ffffff;border:1px solid {LINE};">

   <tr><td style="background:{CHARCOAL};padding:18px 24px;">
     <div style="font:700 12px/1 'Segoe UI',Arial,sans-serif;letter-spacing:2px;color:{RED_BRIGHT};">
       TWO-MINUTE TRAINING TUESDAY
     </div>
     <div style="font:13px/1.4 'Segoe UI',Arial,sans-serif;color:#c6cbd6;padding-top:6px;">
       Episode {number} &middot; {ep['app']} &middot; {ep['runtime']}
     </div>
   </td></tr>

   <tr><td style="padding:24px 24px 4px;">
     <h1 style="margin:0;font:700 22px/1.3 'Segoe UI',Arial,sans-serif;color:{INK};">
       {ep['title']}
     </h1>
   </td></tr>

   <tr><td style="padding:12px 24px 0;">
     <p style="margin:0;font:15px/1.6 'Segoe UI',Arial,sans-serif;color:{INK};">
       {ep['summary']}
     </p>
   </td></tr>

   <tr><td style="padding:20px 24px 0;">
     <table role="presentation" width="100%" cellpadding="0" cellspacing="0"
            style="background:{TINT};border-left:3px solid {RED};">
       <tr><td style="padding:14px 16px;">
         <div style="font:700 11px/1 'Segoe UI',Arial,sans-serif;letter-spacing:1px;
                     color:{RED};padding-bottom:8px;">THE RECAP</div>
         <table role="presentation" cellpadding="0" cellspacing="0">{recap_rows}</table>
       </td></tr>
     </table>
   </td></tr>

   <tr><td style="padding:24px;">
     <table role="presentation" cellpadding="0" cellspacing="0">
       <tr><td style="background:{RED};">
         <a href="{ep['videoUrl']}"
            style="display:inline-block;padding:12px 26px;font:700 15px/1 'Segoe UI',Arial,sans-serif;
                   color:#ffffff;text-decoration:none;">Watch it &rsaquo;</a>
       </td></tr>
     </table>
     {library_line}
   </td></tr>

   <tr><td style="border-top:1px solid {LINE};padding:16px 24px;">
     <p style="margin:0;font:12px/1.6 'Segoe UI',Arial,sans-serif;color:{INK_MUTED};">
       One tip. One video. Under two minutes. Every Tuesday.<br>
       Got a tip you want covered &mdash; ERP, Outlook, Teams, anything? Just reply.
     </p>
   </td></tr>

  </table>
 </td></tr>
</table>
</body></html>"""


def render_text(series: dict, ep: dict, recap: list[str]) -> str:
    """Real plain-text alternative, not a stripped-tags afterthought. Some people
    read mail as text, and search indexes it."""
    lines = [
        f"TWO-MINUTE TRAINING TUESDAY — Episode {ep['number']:03d} · {ep['app']} · {ep['runtime']}",
        "",
        ep["title"],
        "",
        ep["summary"],
        "",
        "The recap:",
    ]
    lines += [f"  {item}" for item in recap]
    lines += ["", f"Watch it: {ep['videoUrl']}"]
    library = series.get("sharePoint", {}).get("folderUrl", "")
    if library:
        lines += ["", f"Every episode: {library}"]
    lines += [
        "",
        "One tip. One video. Under two minutes. Every Tuesday.",
        "Got a tip you want covered — ERP, Outlook, Teams, anything? Just reply.",
    ]
    return "\n".join(lines)


RECAPS = {
    1: [
        "=UNIQUE(range)",
        "=SORT(UNIQUE(range))",
        "=FILTER(table, column = criteria)",
    ],
    2: [
        "Data → Data Validation → Allow: List",
        "Basic source:  =$M$5:$M$10",
        "Live source:   =$O$5#",
    ],
}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--episode", type=int, required=True)
    ap.add_argument("--to", action="append", required=True,
                    help="recipient; repeatable. No default, deliberately.")
    ap.add_argument("--manifest", default="episodes.json")
    ap.add_argument("--dry-run", action="store_true",
                    help="print the HTML and send nothing")
    args = ap.parse_args()

    manifest = load_manifest(Path(args.manifest))
    series = manifest["series"]
    ep = find_episode(manifest, args.episode)

    if not ep.get("videoUrl"):
        sys.exit(f"Episode {args.episode} has no videoUrl. Not sending a dead link.")

    recap = RECAPS.get(ep["number"], [])
    html = render_html(series, ep, recap)
    text = render_text(series, ep, recap)

    if args.dry_run:
        print(html)
        return

    host = os.environ.get("Smtp__Host")
    port = int(os.environ.get("Smtp__Port", "25"))
    if not host:
        sys.exit("Smtp__Host is not set. Source ~/.config/clc-shared/smtp.env.sh first.")

    sender = series["sender"]
    msg = EmailMessage()
    msg["Subject"] = (
        f"Two-Minute Training Tuesday #{ep['number']:03d} — {ep['title']}"
    )
    msg["From"] = formataddr((sender["displayName"], sender["address"]))
    msg["Reply-To"] = sender["address"]

    # BCC, NOT TO -- mirrors SmtpTrainingEmailSender in the Hub. An announcement list on the To
    # line hands every recipient every other address and turns one Reply All into a thread the
    # whole list has to read. The To line carries the sender so the message is not header-less.
    msg["To"] = sender["address"]
    msg["Bcc"] = ", ".join(args.to)

    msg.set_content(text)
    msg.add_alternative(html, subtype="html")

    with smtplib.SMTP(host, port, timeout=30) as smtp:
        # send_message honours Bcc for the envelope but does not transmit the header.
        smtp.send_message(msg)

    print(f"sent episode {ep['number']:03d} to {', '.join(args.to)}")


if __name__ == "__main__":
    main()
