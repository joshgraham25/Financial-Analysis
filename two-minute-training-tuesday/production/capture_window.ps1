<#
.SYNOPSIS
  Capture a single application window at native resolution, for the episode pipeline.

.DESCRIPTION
  Built for 003 and kept because the first version lived in a scratchpad directory and was
  swept between sessions, taking the whole rig with it.

  Uses PrintWindow rather than a screen grab. That matters twice over:

    * It captures the target window only, so nothing else on the desktop can wander into
      frame. The first 003 attempt used Graphics.CopyFromScreen and captured Josh's browser
      instead of Excel, because he was using the machine.
    * It works while the window is not in front, so the capture does not need the machine to
      itself.

  For a browser, drive Chrome into TRUE FULLSCREEN first (-Fullscreen). A page-level F11
  keystroke never reaches the browser chrome; this sends it at the OS level. Fullscreen gives
  a window that is exactly the display size with no tabs, address bar or bookmarks, so the
  frames need no cropping and screen text is never rescaled.

.PARAMETER Name
  Output file name (without extension), written to -OutDir.

.PARAMETER Match
  Regex matched against process MainWindowTitle. Default 'Outlook'.

.PARAMETER WindowClass
  Top-level window class to enumerate. Default 'Chrome_WidgetWin_1', Chrome's frame.
  Excel is 'XLMAIN'. The default is a browser class, so capturing any other app without
  setting this reports "no window matches" while the window is plainly on screen.

.PARAMETER OutDir
  Directory for the PNG. Created if missing.

.PARAMETER Fullscreen
  Send F11 to the matched window at the OS level and return, capturing nothing.

.PARAMETER Size
  "WIDTHxHEIGHT" — move/resize the window and return, capturing nothing. Windowed capture is
  a fallback; the display work area caps the height, which on a 1920x1080 screen leaves well
  under 1080 rows of page. Prefer -Fullscreen.

.EXAMPLE
  .\capture_window.ps1 -Fullscreen
  .\capture_window.ps1 -Name s01_start -OutDir ..\episodes\004-.../frames
#>
[CmdletBinding()]
param(
    [string]$Name,
    [string]$Match = 'Outlook',
    [string]$WindowClass = 'Chrome_WidgetWin_1',
    [string]$OutDir = '.',
    [switch]$Fullscreen,
    [string]$Size
)

$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing

Add-Type @"
using System;
using System.Text;
using System.Collections.Generic;
using System.Runtime.InteropServices;
public class CapWin {
  [DllImport("user32.dll")] public static extern bool PrintWindow(IntPtr h, IntPtr dc, uint f);
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT r);
  [DllImport("user32.dll")] public static extern bool MoveWindow(IntPtr h,int x,int y,int w,int t,bool r);
  [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h,int c);
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
  [StructLayout(LayoutKind.Sequential)] public struct RECT { public int L,T,R,B; }

  [DllImport("user32.dll")] static extern bool EnumWindows(EnumProc cb, IntPtr l);
  [DllImport("user32.dll", CharSet=CharSet.Unicode)] static extern int GetWindowTextW(IntPtr h, StringBuilder s, int c);
  [DllImport("user32.dll", CharSet=CharSet.Unicode)] static extern int GetClassNameW(IntPtr h, StringBuilder s, int c);
  [DllImport("user32.dll")] static extern bool IsWindowVisible(IntPtr h);
  delegate bool EnumProc(IntPtr h, IntPtr l);
  public class Win { public IntPtr Handle; public string Title; }

  public static List<Win> FindWindows(string cls) {
    var found = new List<Win>();
    EnumWindows((h, l) => {
      if (!IsWindowVisible(h)) return true;
      var c = new StringBuilder(256); GetClassNameW(h, c, 256);
      if (c.ToString() != cls) return true;
      var t = new StringBuilder(1024); GetWindowTextW(h, t, 1024);
      if (t.Length > 0) found.Add(new Win { Handle = h, Title = t.ToString() });
      return true;
    }, IntPtr.Zero);
    return found;
  }
}
"@

# Enumerate top-level windows rather than asking Get-Process for MainWindowTitle.
# Chrome spreads its windows across several processes and only reports a title for one
# of them, so the Get-Process form this script used at first could not see a window that
# was plainly on screen -- it failed with "no window matches" while the Outlook window
# was sitting right there. Class name Chrome_WidgetWin_1 is Chrome's top-level frame.
$found = [CapWin]::FindWindows($WindowClass) | Where-Object { $_.Title -match $Match }
if (-not $found) {
    $seen = ([CapWin]::FindWindows($WindowClass) | ForEach-Object { "  - " + $_.Title }) -join "`n"
    throw ("No window whose title matches '$Match'.`nVisible windows of class " +
           "'$WindowClass':`n$seen`n`nNote the title follows the ACTIVE tab -- a " +
           "background tab will not match, so bring the tab you want to the front.")
}
if ($found.Count -gt 1) {
    $list = ($found | ForEach-Object { "  - " + $_.Title }) -join "`n"
    throw "'$Match' matches more than one window; narrow -Match.`n$list"
}
$hwnd = [IntPtr]$found[0].Handle

if ($Fullscreen) {
    [CapWin]::SetForegroundWindow($hwnd) | Out-Null
    Start-Sleep -Milliseconds 600
    (New-Object -ComObject WScript.Shell).SendKeys('{F11}')
    Start-Sleep -Milliseconds 1500
    "fullscreen sent to: $($proc.MainWindowTitle)"
    return
}

if ($Size) {
    if ($Size -notmatch '^(\d+)x(\d+)$') { throw "Size must look like 1936x1400, got '$Size'" }
    [CapWin]::ShowWindow($hwnd, 9) | Out-Null          # SW_RESTORE, out of maximised
    [CapWin]::MoveWindow($hwnd, 0, 0, [int]$Matches[1], [int]$Matches[2], $true) | Out-Null
    Start-Sleep -Milliseconds 800
    $r = New-Object CapWin+RECT
    [CapWin]::GetWindowRect($hwnd, [ref]$r) | Out-Null
    "resized to $($r.R - $r.L)x$($r.B - $r.T) (the work area caps this; use -Fullscreen instead)"
    return
}

if (-not $Name) { throw "Pass -Name, or one of -Fullscreen / -Size." }
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

$r = New-Object CapWin+RECT
[CapWin]::GetWindowRect($hwnd, [ref]$r) | Out-Null
$w = $r.R - $r.L; $h = $r.B - $r.T

$bmp = New-Object Drawing.Bitmap($w, $h)
$g   = [Drawing.Graphics]::FromImage($bmp)
$dc  = $g.GetHdc()
[CapWin]::PrintWindow($hwnd, $dc, 2) | Out-Null        # PW_RENDERFULLCONTENT
$g.ReleaseHdc($dc)
$bmp.Save((Join-Path $OutDir "$Name.png"), [Drawing.Imaging.ImageFormat]::Png)
$g.Dispose(); $bmp.Dispose()

"$Name  ${w}x${h}"
