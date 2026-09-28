<#
.SYNOPSIS
  Drive Excel through COM and capture episode 005's frames.

.DESCRIPTION
  The Outlook episodes drove a browser and captured it; this drives Excel the same way. Only
  the driving changes -- capture_window.ps1 grabs any window by title with PrintWindow, so the
  capture half is unchanged.

  Excel is EASIER to drive than the browser was, and for a reason worth keeping: setting a
  cell value is a single deterministic call with no re-render to race, where the browser
  needed element lookups that went stale between clicks. There is no equivalent here of the
  stale-reference delete that cost Josh a conditional formatting rule.

  What it still shares with the browser rig:
    * The window must be a real 1920x1080 so nothing is rescaled. Screen text is the whole
      reason this series renders frames instead of recording video.
    * Frames are held for the length of the narration later; nothing is recorded in real time.

  Excel-specific setup, all of which has burned an episode before:
    * Zoom 130 -- 100% at 1080p is the ~11px text that got 002 reported as blurry.
    * Ribbon collapsed; the tip is not about a ribbon control.
    * Answer Key sheet hidden. It holds the finished formulas.
    * Gridline/heading state left alone: the viewer needs column letters to follow "column 5".
#>
[CmdletBinding()]
param(
    [string]$Workbook = "$PSScriptRoot\..\episodes\005-excel-xlookup\demo-workbook.xlsx",
    [string]$OutDir   = "$PSScriptRoot\..\episodes\005-excel-xlookup\frames\raw"
)

$ErrorActionPreference = 'Stop'
$cap = Join-Path $PSScriptRoot 'capture_window.ps1'
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
$Workbook = (Resolve-Path $Workbook).Path

function Grab([string]$name) {
    Start-Sleep -Milliseconds 700
    # -WindowClass matters: capture_window.ps1 defaults to Chrome's frame class, so an Excel
    # capture without this reports "no window matches" while Excel is plainly on screen.
    & $cap -Name $name -Match 'Excel' -WindowClass 'XLMAIN' -OutDir $OutDir
}

$xl = New-Object -ComObject Excel.Application
$xl.Visible = $true
$xl.DisplayAlerts = $false
$wb = $xl.Workbooks.Open($Workbook)

# --- window + view -------------------------------------------------------------
$xl.WindowState = -4143                      # xlNormal, so Width/Height apply
$xl.Left = 0; $xl.Top = 0
$xl.Width  = 1920 * 0.75                     # Excel measures in points, 96dpi -> 0.75
$xl.Height = 1080 * 0.75
$xl.ActiveWindow.DisplayGridlines = $true
$xl.ActiveWindow.DisplayHeadings  = $true
try { $wb.Sheets("Answer Key").Visible = 0 } catch { }   # xlSheetHidden

# COLLAPSE the ribbon, do not HIDE it. SHOW.TOOLBAR("Ribbon",False) removes it entirely --
# no File/Home tabs at all -- which is a screen Excel never shows a user, and the series'
# first rule is that what is on screen matches the real app exactly. MinimizeRibbon leaves
# the tab strip, which is what Ctrl+F1 does by hand.
$xl.ExecuteExcel4Macro('SHOW.TOOLBAR("Ribbon",True)')
try {
    if (-not $xl.CommandBars.GetPressedMso('MinimizeRibbon')) {
        $xl.CommandBars.ExecuteMso('MinimizeRibbon')
    }
} catch { }

# The viewer has to be able to tell which sheet they are looking at: the episode moves
# between the export and the report five times, and a frame with no tabs makes that a
# cut rather than a navigation.
$xl.ActiveWindow.DisplayWorkbookTabs = $true
$xl.DisplayStatusBar = $true
$xl.DisplayFormulaBar = $true

$export = $wb.Sheets("ERP Export")
$report = $wb.Sheets("Report")
foreach ($s in @($export, $report)) { $s.Activate(); $xl.ActiveWindow.Zoom = 130 }

# --- 1. the export -------------------------------------------------------------
$export.Activate(); $export.Range("A1").Select()
Grab 's01_export'

# --- 2. the report, empty ------------------------------------------------------
$report.Activate(); $report.Range("A1").Select()
Grab 's02_report'

# --- 3. a VLOOKUP that works ---------------------------------------------------
$report.Range("C5").Formula = "=VLOOKUP(C4,'ERP Export'!A:E,5,FALSE)"
$report.Range("C5").Select()
Grab 's03_vlookup'

# --- 4/5. break it: insert a column into the export ----------------------------
$export.Activate()
$export.Columns("C").Insert() | Out-Null
$export.Range("C1").Value2 = "Revision"
$export.Range("C1").Select()
Grab 's04_inserted'

$report.Activate(); $report.Range("C5").Select()
Grab 's05_wrong'                              # same formula, no error, wrong column

# --- 6. the XLOOKUP ------------------------------------------------------------
$report.Range("C5").Select()
Grab 's06_formulabar'                         # the 5 that moved, in the formula bar

$report.Range("C6").Formula = "=XLOOKUP(C4,ERP_Export[Job No],ERP_Export[Amount])"
$report.Range("B6").Value2 = "Amount (XLOOKUP)"
$report.Range("C6").Select()
Grab 's07_xlookup'

# --- 7. insert another column; XLOOKUP holds -----------------------------------
$export.Activate()
$export.Columns("B").Insert() | Out-Null
$export.Range("B1").Value2 = "Plant"
$export.Range("B1").Select()
Grab 's08_inserted2'

$report.Activate(); $report.Range("C6").Select()
Grab 's09_holds'

# --- 8. looking left -----------------------------------------------------------
# Clear the broken VLOOKUP first. After the SECOND insert its index 5 lands on Part No, so the
# cell labelled "Amount" sits there reading MNT-532 -- true, and a genuinely nice illustration
# that it degrades further, but the script does not say that and an unexplained part number
# under an Amount label just reads as a mistake. The VLOOKUP point is already made; the rest of
# the episode is about XLOOKUP's other two wins, so give them a clean sheet.
$report.Range("C5").ClearContents() | Out-Null

$report.Range("C10").Formula = "=XLOOKUP(C9,ERP_Export[Part No],ERP_Export[Job No])"
$report.Range("C10").Select()
Grab 's10_left'

# --- 9. not found --------------------------------------------------------------
$report.Range("C15").Formula = "=VLOOKUP(C14,'ERP Export'!A:F,5,FALSE)"
$report.Range("C15").Select()
Grab 's11_na'

$report.Range("C15").Formula = "=XLOOKUP(C14,ERP_Export[Job No],ERP_Export[Amount],""Not found"")"
$report.Range("C15").Select()
Grab 's12_notfound'

# --- leave the file on disk untouched ------------------------------------------
$wb.Close($false)            # discard: the workbook is rebuildable from its script anyway
$xl.Quit()
[System.Runtime.InteropServices.Marshal]::ReleaseComObject($xl) | Out-Null
"done -- frames in $OutDir"
