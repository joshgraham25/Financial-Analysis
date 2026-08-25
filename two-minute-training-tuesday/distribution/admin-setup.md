# Setup — what still has to be granted, and by whom

Updated 2026-08-24, after verifying the SharePoint side against the live tenant.
**The SharePoint ask turned out not to need an administrator at all.** Only the
mail identity does, and only if the sender changes from Josh to the finance alias.

---

## 1. SharePoint — where the videos live

### Interim home (do this now): a new library on the TFA site

Access to `CLC Training` on the main site is not available yet, so the series
starts in its own document library on the site Josh already controls:

> `https://creativeliquidcoatingsfw.sharepoint.com/sites/ThomasFAnderson`
> → new document library: **Two-Minute Training Tuesday**

**A new library, deliberately NOT a folder inside the existing Thomas F Anderson
Library.** That library holds per-app *data* folders — `Fleet`, `Finance_OPEX`,
`Checkbook` — and its siblings include `Finance- Locked` and `Management-
Locked`. A staff-facing folder in there means either fighting that inheritance or
breaking it with a per-folder exception, which is precisely the arrangement that
later produces "why can this person see that." A fresh library starts clean and
is set read-for-all-staff in one place.

**Steps:**

1. Create a document library named **Two-Minute Training Tuesday**.
2. Set it **read for all staff**, contribute for the producer.
3. Add one folder per application: `Excel/`, `Outlook/`, `Teams/`, `ERP/`,
   `Windows/` — matching [`../production/publishing.md`](../production/publishing.md).
4. Add the four columns and fill them on every upload:

   | Column | Type | Example |
   | --- | --- | --- |
   | Episode | Number | 2 |
   | App | Choice (Excel / Outlook / Teams / ERP / Windows) | Excel |
   | Tip | Single line of text | Data Validation, spill reference # |
   | Published | Date | 2026-08-25 |

5. Upload each episode's MP4, `.srt`, and demo workbook, then paste the item URL
   into that episode's `videoUrl` in [`../episodes.json`](../episodes.json), set
   `published`, and set `series.sharePoint.folderUrl` to the library root.

**Claude cannot do this part.** The session's Microsoft 365 access is read-only:
search and read, no upload and no library or folder creation.

### Eventual home: `CLC Training` on the main site

Verified 2026-08-24 by listing it — this is already the company's training-video
home, organised one folder per programme:

| Existing folder | Size |
| --- | --- |
| Paulson Training Videos — English and Spanish | 12.8 GB |
| LEHS Training | 13.7 GB |
| CLC University | 5.0 GB |
| IQMS Training Videos | 3.9 GB |
| IQMS Training Guides (+ Spanish) | 0.3 GB |

It is where a staff member looking for training would actually look, which is the
only thing it buys over the interim library — the Hub is the front door people
use day to day.

### The migration rule, and it matters

Re-pointing the Hub after a move is **one file**: update `videoUrl` in
`episodes.json` and drop the manifest on the host. No redeploy, no rebuild — the
section re-reads the manifest when its timestamp changes.

What cannot be updated is **an email that has already been sent.** Those carry
whatever link was current, and moving a file in SharePoint breaks them.

> **When migrating: do not delete the originals.** Leave the interim library in
> place, read-only. Old links keep resolving, new ones point at the new home, and
> nothing mailed in month one dies in month four.

Which also means: migrating is optional. If the interim library is permissioned
correctly and people reach episodes through the Hub, the move buys discoverability
and nothing else. Decide after seeing whether anyone browses SharePoint directly
— not on a schedule.

## 2. Mail — the only real admin ask, and it is currently deferred

**Right now no grant is needed.** The sender is configured as:

> `Two-Minute Training Tuesday <JoshGraham@creativeliquidcoatings.com>`

A display name over an address you own is entirely legitimate — it is not
spoofing, it needs no permission, and it will pass DMARC. It also means the first
sends can be tested immediately.

### If and when the sender becomes "Mr. Bean"

**Do not simply change the display name to Mr. Bean over Josh's address.** That
is exactly the spoofing shape: the envelope still says Josh, so Outlook renders
"Mr. Bean on behalf of Josh Graham", and stricter filters may quarantine it.

To genuinely send as the finance alias:

1. Confirm what the alias actually is — a **shared mailbox**, a **distribution
   list**, or an **M365 group**. This matters: *you cannot send as a distribution
   list.* If that is what Mr. Bean is, a shared mailbox has to be created.
2. Grant **Send As** on that mailbox to the account the Hub authenticates to
   Exchange Online with.
3. Verify on a real send: the received message must show Mr. Bean with **no "on
   behalf of"**, and the headers must show `dmarc=pass`.

### Also still needed for a company-wide send

- **A recipient distribution group.** Not a hand-maintained address list in app
  config — that rots and keeps mailing people who have left.
- **A sanity check on volume.** The platform's Exchange Online direct send is
  currently used for OTP codes: one internal recipient at a time. A company-wide
  send is a different traffic pattern and is what trips connector throttling.

---

## An alternative worth ten minutes before the Send As grant

CLC already has a working **certificate-based Entra app registration** with Graph
clients in the Access Manager app (`GraphCertificateTokenProvider`,
`GraphSharePointReader`). Granting `Mail.Send` **scoped to the single Mr. Bean
mailbox** via an application access policy is arguably cleaner than Send As: the
app authenticates as itself, the permission covers one mailbox rather than an
identity, and it is revocable in one place with Entra audit logging.

SMTP + Send As was chosen and reuses plumbing that already works, which is fine.
This note exists only because that cert infrastructure was found *after* the
decision, which changes the cost comparison.

---

## What is blocked on what

| Item | Blocked by |
| --- | --- |
| Hub section showing playable episodes | `videoUrl` values — i.e. the uploads |
| Any real weekly send | A recipient distribution group |
| Sending as Mr. Bean specifically | Send As, and confirming the mailbox type |
| Building and testing both | **Nothing** |

The email job is designed to refuse to draft an episode whose `videoUrl` is
empty, so it can be built and tested today. That refusal is the behaviour you
want to observe in testing, not a blocker.
