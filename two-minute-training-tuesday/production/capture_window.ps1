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

.PARAMETER Process
  Process name to search. Default 'chrome'.

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
    [string]$ProcessName = 'chrome',
    [string]$OutDir = '.',
    [switch]$Fullscreen,
    [string]$Size
)

$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing

Add-Type @"
using System;
using System.Runtime.InteropServices;
public class CapWin {
  [DllImport("user32.dll")] public static extern bool PrintWindow(IntPtr h, IntPtr dc, uint f);
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT r);
  [DllImport("user32.dll")] public static extern bool MoveWindow(IntPtr h,int x,int y,int w,int t,bool r);
  [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h,int c);
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
  [StructLayout(LayoutKind.Sequential)] public struct RECT { public int L,T,R,B; }
}
"@

$proc = Get-Process $ProcessName -ErrorAction SilentlyContinue |
        Where-Object { $_.MainWindowTitle -match $Match } |
        Select-Object -First 1
if (-not $proc) {
    throw "No '$ProcessName' window whose title matches '$Match'. Open it, and note the title " +
          "follows the ACTIVE tab -- a background tab will not match."
}
$hwnd = $proc.MainWindowHandle

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
