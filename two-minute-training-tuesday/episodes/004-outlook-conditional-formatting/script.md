# Episode 004 — Color-code your inbox without moving a thing

| | |
| --- | --- |
| **Episode** | 004 |
| **App** | Outlook — **new Outlook / Outlook on the web** |
| **Tip** | **Conditional formatting** — a rule that colors matching messages in the list |
| **Target runtime** | 1:45 (ceiling 2:15) |
| **Recorded** | Driven in the browser and captured, per 003 |
| **Recap card** | 1. `Settings → Mail → Conditional formatting` · 2. Name, condition, color · 3. Rules run in order — the first match wins · 4. Nothing moves, nothing is filtered |
| **Demo folder** | `Training samples` · condition `From` · colored sender **Athena Lakis** (Josh, 2026-09-22) |

## Verified in the real dialog, 2026-09-21

Everything below was read out of Outlook itself, not from documentation. 003 cost two rewrites
for being scripted ahead of the UI; this one was checked first.

- **Path:** `Settings → Mail → Conditional formatting`. Microsoft's own blurb:
  *"Create conditional formatting rules to personalize colors of your incoming messages."*
- **`+ Add rule`**, then the same three numbered steps Search Folders uses:
  **1 Name your rule · 2 Condition · 3 Formatting.**
- **The name is required first.** Opening the Condition list with an empty name throws
  *"Please enter a name."* — identical to 003's behaviour, which makes a nice callback.
- **Step 3 shows a live preview row** — a sample message (`Sender name` / `Subject` /
  `Preview text` / `2:55 PM`) that takes the color as you choose it. **This is the shot.**
- **Each saved rule gets** a color dot, an on/off toggle, **Move up / Move down**, edit and
  delete. The arrows matter: rules run in order and the first match wins.

### The conditions on offer, verbatim

| People | Subject | Status | Attachments | Size | Importance |
| --- | --- | --- | --- | --- | --- |
| From | Subject includes | Marked as read | With attachments | Between | High |
| Sender address includes | | Marked as unread | Without attachments | Greater than | Normal |
| Mentions me | | Categorized | | Lower than | Low |
| I'm on the To or Cc line | | Flagged | | | |
| **I'm not on the To line** | | Not flagged | | | |
| I'm on the To line | | Marked as completed | | | |
| I'm on the Cc line | | | | | |

There is also **Prioritized by Copilot**.

**Still to confirm at capture:** the exact wording of the color choices under *Select a
modification*. The dialog will not open that list until the rule has a name and a condition,
and building a throwaway rule in the live mailbox just to read a menu was not worth it.
Confirm on camera and fix the caption if it differs.

## Why this tip, and why it is not just prettier

**Josh already does this** — two rules are live right now, `Stephen/Abe` in red and
`John/Thommy/Caleb` in green, and you can see them working in the message list. A real habit
beats an invented scenario; that is what made 002's cost-center drop-down and 003's ideas
folder land.

**The demo uses `From`** — color one person's mail — which is exactly the rule Josh already
runs. Not because it is the cleverest condition, but because it is the one that *works on safe
content*: the `Training samples` messages are nearly all addressed directly to him, so a to/cc
rule would color nothing and the payoff shot would show no change at all. See
[`demo-folder.md`](demo-folder.md).

> Your inbox does not distinguish between *someone you must not keep waiting* and *everyone
> else*. Both arrive looking identical, and you re-sort them by eye every morning.

**`I'm not on the To line` gets one line near the end** as the other rule worth building — it
fades back everything you were only copied on. Named, not demonstrated.

## The spine, and how it follows 003

Same idea as Search Folders, one step on: **make Outlook organize itself without moving your
mail.** 003 gathered mail without filing it; 004 ranks it without filtering it.

That matters for the closing beat. A rule that *moves* mail hides things from you. A color
hides nothing — everything is still there, still in date order, still one scroll away.

## Structure

**Act 1 — the pain (0:00–0:20).** The list, everything the same weight. Some people you cannot
afford to miss; they look like everything else.

**Act 2 — build it (0:20–1:05).** `Settings → Mail → Conditional formatting → Add rule`. Name
it. Condition: **From**, and the person. Pick a color. Watch the preview row change. Save.

**Act 3 — the payoff (1:05–1:35).** Back to the list: their messages stand out, everything else
is exactly where it was. Nothing moved, nothing was filtered. Then the two footnotes: the
**I'm not on the To line** rule, and the fact that **rules run top to bottom and the first match
wins** — which is what the up and down arrows are for.

## The content problem — solved, by a demo folder

**Josh, 2026-09-22: copy hand-picked safe messages into a folder and record that.** This is
the answer for every Outlook episode from here, not just this one, so it is written up as the
standing pattern in
[`../003-outlook-search-folders/recording-setup.md`](../003-outlook-search-folders/recording-setup.md).

Why it beats what came before: 003's payoff shot was safe only because a Search Folder happened
to hold nothing but training mail, and that luck does not generalise. This episode's natural
payoff is the Inbox — the one view that cannot be sanitized, and the view where a cut of 003
shipped with 401k audit, a subject containing "Confidential Information", K-1s and two LOIs
legible on screen. A curated folder replaces luck with a decision made by the person who knows
what is sensitive.

**Four things to get right when filling it:**

1. **Copy, do not move.** Right-click → *Copy to folder*. Moving reorganizes the real mailbox
   to make a video, and the originals are then missing from where they belong.
2. **Pick for contrast.** `I'm not on the To line` only teaches if some rows color and some do
   not, so the folder needs a genuine mix of direct-to-you and copied-in messages. Check the
   To/Cc line while picking, not afterwards.
3. **Copies keep real senders and subjects.** "Safe" means vetted one by one — which is the
   point, and why this works.
4. **Spread the dates.** A dozen messages all from one afternoon renders as a single flat block;
   a few days apart gives the normal "Today / Last week" headers and looks like a real list.

**Name it something that reads naturally in the folder pane** — a folder called `Demo` or
`Test` on camera undercuts the tip. Josh to choose.

The rest of the pre-flight is unchanged — see
[`../003-outlook-search-folders/recording-setup.md`](../003-outlook-search-folders/recording-setup.md):
preview text off, reading pane hidden, notifications off, Outlook window only, and read every
shot of the finished render before anyone else does.

## Shot list

| Time | Say | On screen |
| --- | --- | --- |
| 0:00 | "Welcome to Two-Minute Training." | The **Training samples** folder |
| 0:05 | "Every one of these looks exactly as important as the others." | Scroll slowly |
| 0:11 | "But there are people whose mail I can't afford to miss." | — |
| 0:16 | "Outlook will mark them for me, if I ask it once." | — |
| 0:21 | "Settings, then Mail, then Conditional formatting." | `Settings → Mail → Conditional formatting` |
| 0:28 | "Add rule." | The **+ Add rule** button |
| 0:32 | "Name it first — it won't let you go on without one." | The name box |
| 0:38 | "Then the condition. There's a whole list of these." | Open **Condition** — hold a beat |
| 0:45 | "From — and the person." | Pick **From**, under People, then **Athena Lakis** |
| 0:51 | "And a color. Watch the sample change as you pick it." | **The preview row recoloring — the shot** |
| 0:59 | "Save." | Save |
| 1:02 | "Now look at the list." | Back to **Training samples**, recolored |
| 1:07 | "Hers stand out. Everything else is exactly where it was." | Rest on it |
| 1:14 | "Nothing moved. Nothing got filtered. Same list, same order." | — |
| 1:20 | "That's the difference from a rule. A rule hides things. This just marks them." | — |
| 1:27 | "There's one for being copied in, too — I'm not on the To line fades those back." | The condition list again, briefly |
| 1:34 | "And they run top to bottom, so the first rule to match wins." | The **Move up / Move down** arrows |
| — | **Over the recap card:** "That's it for this week." | Recap card |
| — | **Over the recap card:** "Next up: VLOOKUP and XLOOKUP." | Recap card |

## The outro — settled

**Josh, 2026-09-21: "Next up: VLOOKUP and XLOOKUP."** So 005 is the lookup episode and the
backlog is renumbered to match. Settled before recording rather than after, which is the whole
point — 003 shipped with an outro nobody had agreed and it cost a re-render.

**Athena Lakis's "get rid of the blank rows" is now passed over twice** (2026-09-01 request,
deferred at 003 and again here) and sits at 006. The backlog's own rule says a tip somebody
asked for jumps the queue, so this is a deliberate override, not drift. Worth a one-line reply
to her — being visibly answered is most of the value of taking requests at all.

## If it runs long, cut in this order

1. The "rules run top to bottom" beat. It is the most advanced thing here and the episode
   survives without it.
2. The "I'm not on the To line" footnote. Useful, but it is a second tip in a one-tip episode.
3. "That's the difference from a rule." Only if desperate — it is the line that stops people
   expecting mail to disappear.

**Never cut** "nothing moved, nothing got filtered." Without it people assume this hides mail,
which is the one wrong idea to leave them with.
