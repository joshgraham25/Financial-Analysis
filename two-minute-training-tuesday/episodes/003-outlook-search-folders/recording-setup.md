# Before you hit record — the Outlook setup

Written after reviewing the 2026-09-17 take (`Outlook Search Folders.mp4`, 4:28), which could not
be used. Every item below is something that take got wrong. None of it is fixable in post, which is
why it is a pre-flight list rather than a style note.

Run through it once, glance at the screen, *then* record.

## The demo folder — the standing answer for Outlook episodes

**Josh, 2026-09-22.** Do not point the camera at a live Inbox. Copy hand-picked, vetted
messages into a folder kept for this, and record that.

This replaces hoping the view happens to be clean. 003's payoff shot was safe only because a
Search Folder happened to contain nothing but training mail — luck, not a method — and the same
episode shipped a cut with 401k audit, a subject reading "Confidential Information", K-1s and
two LOIs legible in the Inbox behind the folder pane.

- **Copy, never move.** Right-click → *Copy to folder*. Moving rearranges the real mailbox to
  make a video and leaves the originals missing from where they belong.
- **Pick for the lesson, not just for safety.** A rule that colors or filters needs rows that
  match and rows that do not, or there is nothing to see. Check that while picking.
- **Copies keep real senders and subjects**, so each one is a judgement — which is exactly why
  a human picks them.
- **Spread the dates** so Outlook renders its normal "Today / Last week" headers instead of one
  flat block.
- **Name it so it reads naturally on camera.** `Demo` or `Test` in the folder pane undercuts
  the tip.
- **Reuse it.** It is a standing asset for every Outlook episode, not a per-episode chore.

## After rendering — read every shot before anyone else does

**This is not optional, and it is the step that failed twice on 003.** Technical checks
(resolution, bitrate, no browser chrome) say nothing about what the frames *say*. Both leaks
that reached a finished render were found by eye, not by a measurement.

1. **Sample the finished MP4 across its whole length** and look at every distinct shot, not
   one frame you happen to trust. The first cut's banner survived because exactly one frame
   was checked and it was the only clean one.
2. **Read the From and Subject columns.** Out loud, if that helps. A cut of 003 shipped with
   the Inbox visible behind the folder pane — 401k audit, a subject containing "Confidential
   Information", K-1s, and two LOIs.
3. **Look at the edges of every dialog.** The settings modal does not cover the window; a
   strip of live mail shows past its right edge, carrying truncated subjects and an invoice
   number.
4. **Re-check after any regeneration.** A mask painted on the frames by hand was silently
   undone when the frames were rebuilt from the raw captures, and the leak returned to a
   render that had already been "fixed". Masks belong in the frame generator, never in a
   post-pass.

## The settings pass — do this first, it does most of the work

Six toggles, all in new Outlook / Outlook on the web. Together they remove every category of
leak except the two named at the bottom, which no setting can reach.

| # | Setting | Where | Why |
| --- | --- | --- | --- |
| 1 | **Message preview text → off** | `Settings → Mail → Layout → Message organization` | Kills the body snippet under every subject line. This is the single biggest one: it is what put "no one should be ordering PC…" and "this is how much tariff with just…" on screen |
| 2 | **Reading pane → Hide** | `Settings → Mail → Layout → Reading pane` | No message body ever renders, including on an accidental click |
| 3 | **Conversation view → off** | `Settings → Mail → Layout` | Messages stop stacking, so clicking one cannot expand a thread of replies you did not plan to show |
| 4 | **Focused Inbox → off** | `Settings → Mail → Layout → Message organization` | One list instead of two tabs. Fewer surprises, and the Inbox shot becomes predictable |
| 5 | **Desktop notifications → off** | `Settings → General → Notifications` | A toast carries a sender and a subject line and lands wherever it likes. Unmissable on camera and impossible to remove afterwards |
| 6 | **Windows Do Not Disturb → on** | Windows notification center | Covers Teams, Outlook desktop and everything else that can pop a toast mid-take |

**What the settings cannot fix — two shots that still need your eyes:**

- **Sender names in the results list.** The Search Folder returns what it returns. Using the
  training-words criteria keeps it to internal training mail by construction, which is exactly why
  the script picks it — but glance at the list before you narrate over it.
- **The Inbox shot.** The "nothing moved" beat needs the real Inbox on screen, with whatever
  arrived that morning sitting around the target message. There is no setting for this. Look at it
  once, immediately before recording, and if the neighbours are awkward, wait an hour or scroll to
  a calmer stretch of the list.

**Folder names in the left pane** are a judgement call rather than a setting. Yours include
people's first names. That is probably fine — a folder called "Tommy" tells nobody anything — but
collapse the account node if you would rather not have the full list parked on screen for two
minutes.

## The blocker — what is legible on screen

**This video goes to a company-wide library. Every subject line in the message list is readable.**

The 2026-09-17 take built a Search Folder for a person, and the results list showed external
customer and supplier correspondence: order-approval complaints, an account dispute, tariff
figures, invoice numbers, VMI consumption. All legible, all with preview text.

- **Demo the scripted folder, not a person.** The words `Two-Minute Training` match internal
  training mail — that is *why* the script picks it. A folder full of customer threads is the one
  result that cannot be shown.
- **Scroll slowly and look at what you are scrolling past.** If a subject line would be awkward on
  a screen in the break room, it is awkward here.

## The frame

- **Record the Outlook window, not the whole screen.** The take captured the full desktop: taskbar,
  every pinned app, the clock, and a "Josh Graham … is signed in" toast sitting over the message
  list in almost every frame.
- **Close the Calendar / To Do pane** on the right. It held a quarter of the frame, showed a real
  meeting schedule with attendee names, and squeezed the actual lesson into the left half.
- **Collapse the folder pane to just what you need**, or at least scroll it so people's names are
  not parked on screen for two minutes.

## The zoom — this is the blurry-video fix

The take was 100% UI at 1920x1080, which puts the message list at roughly 11px. That is exactly
what got 002 reported as blurry: SharePoint serves a reduced rendition to a small player, and
small text does not survive it.

- **Zoom the message list to 150–175%** (`Ctrl + Scroll` over the list).
- **Then look at it at half size.** If you cannot read a subject line in a window a quarter of your
  screen, neither can the audience.

## The take itself

- **Know the path before you start.** The 2026-09-17 take lost about ninety seconds wandering
  through `Settings → Accounts` looking for Search Folders. Click through the whole sequence once
  with the recorder off.
- **Pause about a second between lines, and do not pause mid-line.** That pause is the only signal
  the tooling has for where one caption ends and the next begins.
- Delivery does not matter. Your audio is a metronome and never ships — Andrew speaks the final cut.
