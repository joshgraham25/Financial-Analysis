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
