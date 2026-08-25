# Setup — what still has to be granted, and by whom

Updated 2026-08-24, after verifying the SharePoint side against the live tenant.
**The SharePoint ask turned out not to need an administrator at all.** Only the
mail identity does, and only if the sender changes from Josh to the finance alias.

---

## 1. SharePoint — Josh can do this himself

**Home: `CLC Training` on the main site.**

> `https://creativeliquidcoatingsfw.sharepoint.com/sites/CLCMainSite`
> → `Shared Documents` → `CLC Training`

Verified 2026-08-24 by listing the folder. It is already the company's
training-video home:

| Existing folder | Size |
| --- | --- |
| Paulson Training Videos — English and Spanish | 12.8 GB |
| LEHS Training | 13.7 GB |
| CLC University | 5.0 GB |
| IQMS Training Videos | 3.9 GB |
| IQMS Training Guides (+ Spanish) | 0.3 GB |
| CLC Training Information / IT Information | small |

So multi-gigabyte video libraries already live here, organised one folder per
programme, and this is where a staff member looking for training would actually
look.

**This replaces the earlier plan to use the Thomas F Anderson Library.** That
library holds per-app *data* folders — `Fleet`, `Finance_OPEX`, `Checkbook`, with
`Finance- Locked` and `Management- Locked` siblings. It is app plumbing, not an
audience-facing space, and its inherited permissions are unlikely to be right for
"every employee can watch this." Working files can still live there if useful;
the copies people watch belong in `CLC Training`.

**Asks — all doable without an administrator:**

1. Create a folder **`Two-Minute Training Tuesday`** inside `CLC Training`,
   alongside `CLC University` and the rest.
2. Inside it, one subfolder per application, matching
   [`../production/publishing.md`](../production/publishing.md): `Excel/`,
   `Outlook/`, `Teams/`, `ERP/`, `Windows/`.
3. Add these columns and fill them on every upload — this is what keeps the
   catalogue searchable at episode thirty instead of a junk drawer:

   | Column | Type | Example |
   | --- | --- | --- |
   | Episode | Number | 2 |
   | App | Choice (Excel / Outlook / Teams / ERP / Windows) | Excel |
   | Tip | Single line of text | Data Validation, spill reference # |
   | Published | Date | 2026-08-25 |

4. Upload each episode's MP4, its `.srt`, and its demo workbook. Then paste the
   item URL into that episode's `videoUrl` in
   [`../episodes.json`](../episodes.json), and set `published`.
5. Check what the folder inherits for permissions — read for all staff is the
   intent. Worth confirming rather than assuming, since sibling folders in other
   libraries are explicitly restricted.

**Claude cannot do this part.** The Microsoft 365 access available to the session
is read-only — search and read, no upload and no folder creation. The one way to
automate it would be the Hub uploading via Graph with `Sites.ReadWrite.All` on
the existing certificate app registration, which is a build plus a permission
grant, not a five-minute job.

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
