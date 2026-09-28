"""Build the on-screen demo workbook for Two-Minute Training episode 005 (XLOOKUP).

    pip install openpyxl
    python build_demo_workbook.py

Output: demo-workbook.xlsx

Stands in for a job-cost export so the episode records with no real customer,
vendor or employee data on screen -- same approach as 001 and 002.

THE LAYOUT IS THE EPISODE. Two things have to be true or the demo does not work:

1. The return column must be far enough right that a column inserted to its LEFT
   changes its position. Amount sits in column E (the 5th), so `VLOOKUP(...,5,FALSE)`
   is correct until someone inserts anywhere in A:E, after which 5 points at
   Cost Center and returns a number that is still a number. No error, wrong answer.
   That silence is the whole point of the episode.

2. The look-left demo needs a column the viewer would plausibly search BY that sits
   to the RIGHT of what they want back. Part No is column C, Job No is column A, so
   "given a part, which job is it on?" is impossible for VLOOKUP and ordinary for
   XLOOKUP.

Cost Center is deliberately NUMERIC. If it were text, the broken VLOOKUP would
return something obviously wrong and the viewer would spot it instantly -- which
would make the episode comforting and useless. A plausible wrong number is the
thing people actually ship.

Fixed seed, so re-running produces the same workbook and the script's references
stay accurate.

Sheets
------
ERP Export   ~40 rows, table ERP_Export. Deliberately short: the viewer must be
             able to see that the answer is wrong, which means being able to read
             the row it came from. 380 rows would hide the point.
Report       The staging area the formulas are typed into on camera.
Answer Key   Finished formulas, for rehearsal. KEEP OFF SCREEN while recording.
"""

from __future__ import annotations

import random
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo

SEED = 20260928
ROWS = 40

RED = "A8121F"
INK = "15171C"
LINE = "D5DAE2"

CUSTOMERS = ["Northwind Trailer", "Lakeshore Fabrication", "Provost Industrial",
             "Bellweather Tool", "Cardinal Stamping", "Halstead Motive",
             "Ironwood Components", "Meridian Plastics"]
PARTS = ["HSG-{:03d}", "BRK-{:03d}", "PLT-{:03d}", "CVR-{:03d}", "MNT-{:03d}"]
CENTERS = [1100, 1200, 1300, 2100, 2200, 3100]

HEAD = ["Job No", "Customer", "Part No", "Cost Center", "Amount"]


def build() -> Workbook:
    rnd = random.Random(SEED)
    wb = Workbook()

    ws = wb.active
    ws.title = "ERP Export"
    thin = Side(style="thin", color=LINE)

    for c, name in enumerate(HEAD, start=1):
        cell = ws.cell(row=1, column=c, value=name)
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor=RED)
        cell.alignment = Alignment(horizontal="center")

    jobs = []
    for i in range(ROWS):
        job = f"J-{4200 + i * 7}"
        jobs.append(job)
        ws.cell(row=i + 2, column=1, value=job)
        ws.cell(row=i + 2, column=2, value=rnd.choice(CUSTOMERS))
        ws.cell(row=i + 2, column=3, value=rnd.choice(PARTS).format(rnd.randint(100, 999)))
        ws.cell(row=i + 2, column=4, value=rnd.choice(CENTERS))
        amt = ws.cell(row=i + 2, column=5, value=round(rnd.uniform(850, 24_000), 2))
        amt.number_format = "#,##0.00"

    for row in ws.iter_rows(min_row=1, max_row=ROWS + 1, max_col=5):
        for cell in row:
            cell.border = Border(bottom=thin)

    table = Table(displayName="ERP_Export", ref=f"A1:E{ROWS + 1}")
    table.tableStyleInfo = TableStyleInfo(name="TableStyleLight1", showRowStripes=True)
    ws.add_table(table)

    for col, width in zip("ABCDE", (12, 24, 12, 14, 14)):
        ws.column_dimensions[col].width = width
    ws.freeze_panes = "A2"

    # --- Report -------------------------------------------------------------
    rp = wb.create_sheet("Report")
    rp["B2"] = "Look up a job"
    rp["B2"].font = Font(bold=True, size=14, color=INK)
    rp["B4"] = "Job No"
    rp["C4"] = jobs[11]                      # a job that exists, mid-table
    rp["B5"] = "Amount"
    rp["B7"] = "Look up a part"
    rp["B7"].font = Font(bold=True, size=14, color=INK)
    rp["B9"] = "Part No"
    rp["C9"] = ws.cell(row=13, column=3).value   # same row, so the two demos agree
    rp["B10"] = "Job No"
    rp["B12"] = "A job that isn't there"
    rp["B12"].font = Font(bold=True, size=14, color=INK)
    rp["B14"] = "Job No"
    rp["C14"] = "J-9999"
    rp["B15"] = "Amount"

    for r in (4, 5, 9, 10, 14, 15):
        rp.cell(row=r, column=2).font = Font(bold=True, color=INK)
    for r in (5, 10, 15):
        rp.cell(row=r, column=3).number_format = "#,##0.00"
    rp.column_dimensions["B"].width = 22
    rp.column_dimensions["C"].width = 18

    # --- Answer Key ---------------------------------------------------------
    ak = wb.create_sheet("Answer Key")
    ak["A1"] = "KEEP THIS SHEET OFF SCREEN WHILE RECORDING"
    ak["A1"].font = Font(bold=True, color=RED)
    for r, (label, formula) in enumerate([
        ("The VLOOKUP that works",      '=VLOOKUP(C4,\'ERP Export\'!A:E,5,FALSE)'),
        ("...and silently breaks",      'insert a column anywhere in A:E -- 5 now points at Cost Center'),
        ("XLOOKUP, same answer",        "=XLOOKUP(C4,ERP_Export[Job No],ERP_Export[Amount])"),
        ("Looking left",                "=XLOOKUP(C9,ERP_Export[Part No],ERP_Export[Job No])"),
        ("If not found",                '=XLOOKUP(C14,ERP_Export[Job No],ERP_Export[Amount],"Not found")'),
    ], start=3):
        ak.cell(row=r, column=1, value=label).font = Font(bold=True)
        ak.cell(row=r, column=2, value=formula)
    ak.column_dimensions["A"].width = 26
    ak.column_dimensions["B"].width = 72

    return wb


if __name__ == "__main__":
    out = Path(__file__).with_name("demo-workbook.xlsx")
    build().save(out)
    print(f"wrote {out.name}")
    print("Check before recording: Answer Key sheet hidden, zoom 130-150%, ribbon collapsed.")
