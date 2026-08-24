# Post copy — episode 002

Ready to paste. The Teams version carries the searchable detail; the Viva version
is deliberately shorter.

---

## Teams channel post

**Two-Minute Training Tuesday #002 — Data Validation, basic and self-maintaining**

> Last week's report ended on a cost-center drop-down. Confession: those six
> names were typed in by hand, which means the day someone adds a cost center,
> the drop-down is wrong and nobody finds out.
>
> 1:55, and it is two techniques, not one:
>
> Every drop-down in Excel is the **Data Validation** feature, and there are
> two ways to feed it.
>
> **Basic** — select the cell, **Data → Data Validation → Allow: List**, and set
> **Source** by selecting the range your list sits in: `=$J$5:$J$10`. Works in
> any version of Excel. Also goes stale silently, because the range you picked
> does not grow when the data does.
>
> **Self-maintaining** — put `=SORT(UNIQUE(ERP_Export[Cost Center]))` in a cell,
> then set **Source** to `=$K$5#`
>
> That `#` is the whole trick. It is a *spill reference* — it means "this cell and
> every cell this formula filled," so the list grows and shrinks with the data by
> itself. Add a cost center to the export and it is in the drop-down with no
> edit. You can hide the helper column; the reference still works.
>
> The basic version works in any Excel; the `#` needs Microsoft 365. Use
> `=$K$5#` with the dollar signs — a relative reference
> gives you an empty drop-down and no error message.
>
> Demo workbook attached if you want to try it on something real.

---

## Viva Engage post

> 1:47. That drop-down on your report was typed in by hand, so it goes stale the
> moment someone adds a cost center.
>
> `=SORT(UNIQUE(range))` for the list, then **Data → Data Validation** → Allow:
> List → Source `=$K$5#`. The `#` means "and everything this formula spilled
> into," so the drop-down maintains itself. Data Validation is the feature
> name — worth knowing, it is behind every drop-down you have ever used.
>
> What else in your week is a list somebody typed once and nobody has updated
> since? Ask below and it goes in the queue.

---

## SharePoint library metadata

| Column | Value |
| --- | --- |
| Episode | 2 |
| App | Excel |
| Tip | Data Validation, spill reference `#` |
| Published | *(the Tuesday you post)* |

---

## Note on posting this one

Post it as a **new conversation**, not a reply to 001 — replies bury. But do link
back to 001 in the first line, because this episode only makes sense as a
follow-up and the callback is what makes the series feel like a series rather
than a pile of tips.
