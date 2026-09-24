# The demo folder — candidates for review

**Josh to review, then copy.** I cannot do either step for you: the Outlook connector in this
session creates *categories*, not folders, and it can only **move** messages, never copy —
moving would rearrange your real mailbox to make a video. Browser access is signed out.

## What I searched, and what it found

I went looking for innocuous internal mail across the whole mailbox. The honest result: **you
are the CFO, and almost nothing in your mailbox is innocuous.** Searches for benign topics
returned consolidated financial statements, insurance due diligence, a customer on-site
security assessment, open purchase-order reports, plant dashboards and labor data. None of it
can go on a company-wide video.

So the folder should be built from the one pool that is safe *by definition*.

## Recommended contents — the Two-Minute Training threads

**Everyone already received these.** They are the series' own emails and the replies to them,
so there is no judgement call to make and nothing to vet line by line. Better still, they carry
real sender variety, which is what a color rule needs to look like anything:

| Sender | Subject | Date |
| --- | --- | --- |
| Athena Lakis | RE: …#001 — training request - remove blanks | 2026-09-01 |
| James Canterbury | RE: …#001 — Stop using copy and pasting to get a unique list | 2026-09-01 |
| Stacy Deckrosh | RE: …#001 — Stop using copy and pasting to get a unique list | 2026-09-01 |
| Samantha Vanhook | RE: …#002 — Data Validation… | 2026-09-10 |
| Thomas Feddeler | Re: …#002 — Data Validation… | 2026-09-10 |
| Jennifer Wilson | RE: …#002 — Data Validation… | 2026-09-10 |
| Holly Sims · Dylan Young · Lucielly Garcia · Julie Harrold · Bernie Salas | RE: …#001 | 2026-09-01 |
| Josh Graham | Fw: …#001 and #002 (several) | 08-25 → 09-10 |

That is **ten or more distinct senders across two dates**, which renders with normal "Last
week / This month" headers rather than one flat block.

**Two more for visual variety**, both already company-wide:

| Muhammad Khan | CLC Town Hall Meeting — Friday, August 14th, 10:00 am | 2026-08-02 |
| Josh Graham | Game Testing (the conference games invite) | 2026-07-01 |

## The problem this creates — and the fix (SETTLED: option 1)

**These messages are nearly all addressed directly to you.** The replies are replies *to Josh*,
so you are on the To line for essentially all of them. That means the condition the script
currently teaches — **`I'm not on the To line`** — would color **nothing**, and the payoff shot
would show no change at all.

Two ways out:

1. **Change the demo condition to `From`.** Color one person's mail — say Athena's — and let
   everything else stay plain. Instant, obvious contrast on completely safe content, and it is
   *exactly what Josh already does* with the live `Stephen/Abe` and `John/Thommy/Caleb` rules.
   Then name "I'm not on the To line" in one line as the one to go and build. **Recommended.**
2. **Add some copied-in mail.** Find a handful of threads where you were only on Cc and are
   happy to show them. Keeps the stronger tip as the demo, but puts the vetting burden back on
   you and reintroduces the risk this folder exists to remove.

**Josh, 2026-09-22: option 1 — condition `From`, folder `Training samples`.** The lesson does not weaken — the mechanism is identical, and
"color the person whose mail you must not miss" is more relatable than a to/cc distinction.

## What to do

1. **Create the folder `Training samples`** — right-click the account → *New folder*.
2. **Copy, do not move.** Right-click a message → *Copy to folder*, or Ctrl+drag. The table
   above is the list; every one of them is mail the whole company already received.
3. **The colored sender is Athena Lakis** (Josh, 2026-09-22). She sent the training request,
   she already appears in 003, and "mail I can't afford to miss" reads as a compliment rather
   than a flag.
4. **Sign back into Outlook in Chrome** and I can do the capture.

Script and lines are already updated for `From` and `Training samples`.

## Still unconfirmed

- Whether the To/Cc split above is exactly right — the search returns sender and subject but not
  recipients, so the "nearly all addressed to you" claim is inferred from the reply structure,
  not read off each message. Worth a glance while you copy them.
- The exact wording of the color choices under *Select a modification*, and that conditional
  formatting colors this folder as expected. Both confirmed on camera.
