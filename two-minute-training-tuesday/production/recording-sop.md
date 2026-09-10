# Recording SOP — Snipping Tool + Clipchamp

Everything here is already on a Windows 11 machine with Microsoft 365. No
purchase, no install, no IT ticket.

- **Snipping Tool** records the screen and your microphone to an MP4.
- **Clipchamp** trims the MP4, adds the title and recap cards, generates
  captions, and exports the final file.

Total hands-on time once you have done it twice: about 25 minutes per episode.

---

## Part 0 — One-time setup (do this once, ever)

### Aspect ratio: shoot 16:9, not vertical

"Short form" here means *short*, not *vertical*. A spreadsheet cropped to 9:16
loses the columns that make the tip make sense, and most of this audience
watches on a desktop or in Teams. Shoot **1920×1080, 16:9**. If you later want a
teaser for a phone-heavy channel, crop a 1:1 square out of the middle in
Clipchamp — do not reshoot.

### Make the screen legible before you ever hit record

This is the single highest-value step, and the one most people skip. Fixing
small text in post is painful; making it big before recording is free.

1. **Settings → System → Display → Display resolution → 1920×1080.** Recording a
   4K monitor and exporting to 1080p shrinks every glyph by half.
2. **Excel zoom to 130–150%** (bottom-right slider, or Ctrl + scroll wheel). Rows
   should look almost comically large on your monitor. They will look correct in
   the finished video.
3. **Collapse the ribbon** (Ctrl+F1) unless the tip is *about* a ribbon button.
   It buys you six more rows of visible data.
4. **Hide the formula bar** only if the tip is not about a formula. For Excel
   formula episodes, leave it up — it is the star of the shot.

### Silence the machine

One Teams toast in frame means a re-record, or a clumsy cut.

1. **Settings → System → Notifications → Do not disturb: On.**
2. Set Teams to **Do not disturb**.
3. Close Outlook entirely. A mail preview in the corner of frame is a data leak,
   not just a distraction.
4. Sign out of, or fully close, anything showing customer or employee names that
   is not part of the demo.

### Set up your recording profile

Record from a clean Windows profile or a clean desktop:

- Desktop with no personal files visible.
- Browser with no bookmark bar full of personal links.
- Use the episode's demo workbook, never a live production file. The demo
  workbook exists so you never have to blur anything.

### Microphone

A $30 USB headset beats a laptop mic by a wide margin — the laptop mic picks up
the fan and the room. Test with **Settings → System → Sound → Input → Test your
microphone**; speaking normally should push the bar to roughly two-thirds. Record
with a door closed; hard empty rooms echo.

---

## Part 1 — Rehearse before you record

Non-negotiable, and it is what keeps episodes under two minutes.

1. Read the script out loud once, at your real speaking pace, while doing the
   clicks. **Time it with a stopwatch.**
2. Over 1:50? Cut words, not steps. The most common fix is deleting the
   explanation of *why* the formula works and letting the result speak.
3. Do the click path twice more until your hands know it. Hunting for a menu on
   camera costs ten seconds of viewer patience every time.

Rehearsal is 5 minutes and routinely saves 40.

---

## Part 2 — Record with Snipping Tool

1. Press **Win + Shift + R**, or open **Snipping Tool** and switch to the
   **Record** (camcorder) mode.
2. Drag a rectangle around the area to capture. **Include a little empty space
   around the Excel window** — a rectangle snapped tight to the window edge looks
   cramped, and you can always crop in.
3. Turn on the **microphone** icon in the recording toolbar. Leave **system
   audio** off unless the tip involves a sound (a Teams call ring, a notification
   chime). System audio on means your own fan noise and every UI blip lands in
   the track.
4. Hit **Start**, then **wait three full seconds in silence** before you speak or
   click. Those three seconds are your editing handle — they give Clipchamp
   something clean to cut against.
5. Deliver the script. **When you fumble, do not stop.** Pause, stay silent for
   two seconds, and redo that sentence from its beginning. Silence is a visible
   marker on the Clipchamp timeline, so retakes become trivial to find and cut.
   Stopping and restarting the whole recording is what turns a 25-minute job into
   a 90-minute one.
6. Wait three silent seconds after your last word, then **Stop**.
7. The MP4 lands in **Videos → Screen Recordings**. Rename it immediately:
   `TMTT-001-raw.mp4`.

### Recording the ERP or anything with real data

Same process, with two additions:

- Use a **sandbox or test company** in the ERP if one exists. If it does not, use
  your own test records — a job number you created for this purpose.
- Before recording, do a **dry pass and look at every corner of the frame** for a
  customer name, a dollar figure, or an employee record that should not be
  published internally. Blurring in Clipchamp is possible but ugly; framing it
  out is better.

---

## Part 3 — Edit in Clipchamp

Open Clipchamp (Start menu, or clipchamp.com signed in with your work account),
**Create a new video**, and confirm the project is set to **16:9**.

### 1. Import and lay down the take

Drag `TMTT-001-raw.mp4` onto the timeline.

### 2. Cut the dead air and the fumbles

Play through once with the audio waveform visible. Every retake you left is a
flat silent gap in the waveform — obvious on sight.

- Position the playhead, press **S** to split, select the bad chunk, press
  **Delete**.
- Clipchamp closes the gap automatically.
- Trim the head and tail so the video starts about half a second before your
  first word.

Cut hard. A 2:10 rough cut almost always has 20 seconds of "um", mouse
wandering, and dead air in it.

### 3. Add the title card

1. Open **`assets/title-card.html`** in a browser, fill in the episode number and
   title, and screenshot it (Win + Shift + S, full screen) — or use the built-in
   PNG download button.
2. Drag the PNG onto the timeline **before** the video clip.
3. Set its duration to **2.5 seconds**. Not longer. Two minutes is the budget.

### 4. Add the recap card

Same generator, "Recap" mode, listing the two or three formulas or steps. Drop
it at the very end, **4 seconds**, so people have time to screenshot it. This
frame gets more reuse than the rest of the video combined.

### 5. Zoom — do it in Excel, not in Clipchamp

Clipchamp has no true keyframed follow-the-cursor zoom. If you set up the screen
per Part 0, you will not need one. When you genuinely must emphasise one cell:

- Select the clip, open **Crop** (or the **Pan and zoom** effect), and crop into
  the region of interest.
- Split the clip so the crop applies only to the seconds that need it.

Better: for a formula close-up, **type the formula in an oversized cell** in the
demo workbook rather than zooming in post.

### 6. Captions

Open **Captions** in the right-hand panel and generate them automatically. Then
**read every line**. Auto-captions reliably mangle exactly the words this series
cares about: `UNIQUE`, `FILTER`, `XLOOKUP`, and every vendor name. Fix them.

Burn the captions in. Most of this audience will watch with sound off at their
desk, and a Teams-embedded video does not always surface a sidecar caption file.

### 7. Export

**Export → 1080p → MP4.** Save as `TMTT-001-Excel-Dynamic-Arrays.mp4`.

Then **watch the exported file, all the way through, once.** Not the preview —
the export. This is where you catch the caption typo and the notification toast.

---

## Part 4 — Publish

See [`publishing.md`](publishing.md).

---

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| Text unreadable in the export | Recorded a high-DPI screen, exported to 1080p | Drop display to 1920×1080 and raise Excel zoom *before* recording. Not fixable in post. |
| No voice in the recording | Mic muted in the Snipping Tool toolbar | Check the mic icon is enabled every single time. Record 5 seconds and play it back before the real take. |
| Audio drifts out of sync on a long take | Long single recordings occasionally drift | Keep takes under about 5 minutes. Two-minute episodes should never hit this. |
| Video feels frantic | Speaking too fast to hit 2:00 | The script is too long. Cut a step, don't talk faster. |
| Captions mangle formula names | Auto-caption doesn't know Excel | Always proofread. Consider spelling it out once verbally: "UNIQUE — U, N, I, Q, U, E". |

---

## The overlay pipeline (from 2026-09-08 — this is now the default)

**Josh records the real application; `overlay_episode.py` adds the wrapper.** The
synthetic renderer is retired for new episodes: a drawn Excel is a drawing of Excel, and
Rule 0 in the style guide asks for one hundred percent. A recording is the only thing
that gets there.

### What Josh does

1. **Record silent.** No microphone. The voiceover is generated from the beats table so
   it stays in sync and can be re-cut without re-recording. (If you do narrate, the tool
   keeps your audio and shifts it past the title card — but then the caption times have
   to be matched to your speech by hand, which is the slow way.)
2. **1920x1080.** Record the whole screen at 1080p. Anything else gets letterboxed.
3. **Nothing but the app.** No captions, no text, no transitions, no music, no zooms in
   Clipchamp. Export the raw capture. Every overlay is added afterwards, from the
   catalogue and the beats file, so it is identical across episodes.
4. **Follow the shot list** in the episode's `script.md`, in order, and **pause for about
   a second between beats.** The pauses are what make caption placement easy and what
   stop the video feeling rushed.
5. **Keep it under 1:53.** The title card (2.5 s) and recap card (4.0 s) add 6.5 s, and
   the ceiling is 2:00.
6. **Export MP4 1080p** and drop it in the episode folder as `raw-recording.mp4`.

Housekeeping before recording: close Outlook and Teams notifications, use the generated
demo workbook (not a real one), and check nothing in frame carries customer or employee
names — this ends up in a company-wide library.

### What the tool does

```bash
python production/overlay_episode.py --episode 2 --video raw-recording.mp4 --check
python production/overlay_episode.py --episode 2 --video raw-recording.mp4
```

`--check` writes the two cards plus overlaid stills into `<episode>/overlay-check/` and
stops. **Always run it first** — it is seconds, and it shows whether the beat times match
what is actually on screen. Then drop `--check` for the real encode.

Title and recap text come from `episodes.json`, so they are written once and cannot drift
from the email or the Hub. Captions come from `<episode>/beats.md`, whose times are the
**recording's own clock** — each caption runs until the next beat starts.

The tool refuses to run if a beat starts after the recording ends, which is the failure
you get from reusing a previous script's timecodes.

### Record in your own voice, ship Andrew's (Josh's idea, 2026-09-08)

Recording silent means guessing where the captions go. So don't: **talk through the
script while you record**, and your voice becomes the metronome without ever shipping.

```bash
python production/beats_from_speech.py --video raw-recording.mp4 --lines lines.md
python production/overlay_episode.py --episode 2 --video raw-recording.mp4 --check
python production/overlay_episode.py --episode 2 --video raw-recording.mp4
```

`beats_from_speech.py` finds where each line starts by detecting the pauses between
them, pairs those times with the script lines, and writes `beats.md`. Then
`overlay_episode.py` speaks those lines in Andrew's voice at those exact times, and your
scratch audio is discarded -- generated audio wins over the recording's own track.

**It calibrates the pause threshold itself.** Verified against a known 19-beat track: at
0.4 s it found 29 stretches (internal pauses split lines) and at 0.9 s it found 18 (two
lines ran together). Neither is usable, and neither is guessable in advance -- so it
detects every pause once and then picks the pause length that yields exactly as many
stretches as there are script lines. It chose 0.70 s and matched all 19 to within 0.4 s
of their real starts.

If it cannot find a threshold that matches, it prints the detected stretches beside the
script lines and stops rather than silently mis-pairing. That means a line got split or
two ran together: re-record that stretch, or pass `--min-gap` yourself.

**While recording:** pause about a second between lines, and don't pause mid-line. That
pause is the entire signal. Speaking naturally is fine -- the words are never used, only
their timing.

---

## Rule 1 of recording: make the text big enough to survive the player

**Added 2026-09-10 after viewers reported 002 was "very blurry until full screen".**
This is the single most important capture setting, ahead of framing, ahead of audio.

**Why.** SharePoint transcodes every upload into an adaptive ladder and the player picks a
rendition to fit its window. Embedded in a page at a few hundred pixels tall, it serves
540p or less and only steps up to 1080p in full screen. At Excel's default 100% zoom, cell
text is about **11 pixels tall**; halve that for a 540p rendition and it is gone. Going full
screen fixed it for viewers because that is when the player finally fetches 1080p.

**A better encode does not rescue this.** 002's master was re-encoded from 464 kbps to
604 kbps with `-tune stillimage`, and CRF 12 only reaches 859 kbps — the Clipchamp source
itself sustains about 1.3 Mbps over static frames, and no encoder invents detail the capture
never had. Small text stays small.

**So, before recording:**

1. **Zoom the application to 150–175%.** Excel's zoom slider, bottom right, or `Ctrl+Scroll`.
   Outlook's message list takes `Ctrl+Scroll` too.
2. **Record a window, not the whole screen.** Every pixel spent on the taskbar, the ribbon
   you are not using, and 40 empty columns is a pixel not spent on the thing you are
   teaching. A maximised Excel window at 1080p is fine; a 4K desktop scaled down is not.
3. **Scroll so only the columns in play are visible.** 002 showed columns A through AD and
   used four of them.
4. **Check it at the size people watch.** Play the finished file in a window about a third
   of the screen. If you cannot read a cell value, neither can they — and most of them will
   never click full screen.

**The one thing to say in the email**, until a recording is captured this way: *"Full screen
makes it much sharper."* It costs a line and it is true of the SharePoint player generally.
