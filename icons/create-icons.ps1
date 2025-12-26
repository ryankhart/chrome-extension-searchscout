Add-Type -AssemblyName System.Drawing

function Create-Icon {
    param([int]$size, [string]$path)

    $bitmap = New-Object System.Drawing.Bitmap($size, $size)
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    $graphics.SmoothingMode = 'AntiAlias'

    # Blue background
    $graphics.Clear([System.Drawing.Color]::FromArgb(26, 115, 232))

    # Draw magnifying glass circle
    $penWidth = [Math]::Max(1, $size / 12)
    $pen = New-Object System.Drawing.Pen([System.Drawing.Color]::White, $penWidth)
    $circleSize = $size * 0.5
    $circleOffset = $size * 0.15
    $graphics.DrawEllipse($pen, $circleOffset, $circleOffset, $circleSize, $circleSize)

    # Draw handle
    $handleStart = $circleOffset + $circleSize * 0.75
    $handleEnd = $size * 0.85
    $graphics.DrawLine($pen, $handleStart, $handleStart, $handleEnd, $handleEnd)

    $graphics.Dispose()
    $bitmap.Save($path, [System.Drawing.Imaging.ImageFormat]::Png)
    $bitmap.Dispose()
}

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Create-Icon 16 (Join-Path $scriptDir "icon16.png")
Create-Icon 32 (Join-Path $scriptDir "icon32.png")
Create-Icon 48 (Join-Path $scriptDir "icon48.png")
Create-Icon 128 (Join-Path $scriptDir "icon128.png")

Write-Host "Icons created successfully"
