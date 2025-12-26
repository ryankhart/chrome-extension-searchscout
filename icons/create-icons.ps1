Add-Type -AssemblyName System.Drawing

function Create-Icon {
    param([int]$size, [string]$path)

    $bitmap = New-Object System.Drawing.Bitmap($size, $size)
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    $graphics.SmoothingMode = 'AntiAlias'

    # Blue background
    $graphics.Clear([System.Drawing.Color]::FromArgb(26, 115, 232))

    # Calculate dimensions for top-down binoculars view
    $tubeWidth = [Math]::Max(6, $size * 0.22)
    $tubeHeight = [Math]::Max(12, $size * 0.65)
    $cornerRadius = [Math]::Max(3, $size * 0.08)
    $spacing = [Math]::Max(2, $size * 0.06)

    # Center the binoculars
    $totalWidth = ($tubeWidth * 2) + $spacing
    $startX = ($size - $totalWidth) / 2
    $startY = ($size - $tubeHeight) / 2

    # Calculate positions
    $rightX = $startX + $tubeWidth + $spacing
    $eyepieceHeight = [Math]::Max(2, $size * 0.08)
    $bottomY = $startY + $tubeHeight - $eyepieceHeight

    # Draw left tube (orange rounded rectangle)
    $leftRect = New-Object System.Drawing.RectangleF($startX, $startY, $tubeWidth, $tubeHeight)
    $leftPath = New-Object System.Drawing.Drawing2D.GraphicsPath
    $diameter = $cornerRadius * 2
    $leftPath.AddArc($leftRect.X, $leftRect.Y, $diameter, $diameter, 180, 90)
    $leftPath.AddArc($leftRect.Right - $diameter, $leftRect.Y, $diameter, $diameter, 270, 90)
    $leftPath.AddArc($leftRect.Right - $diameter, $leftRect.Bottom - $diameter, $diameter, $diameter, 0, 90)
    $leftPath.AddArc($leftRect.X, $leftRect.Bottom - $diameter, $diameter, $diameter, 90, 90)
    $leftPath.CloseFigure()

    # Draw right tube (orange rounded rectangle)
    $rightRect = New-Object System.Drawing.RectangleF($rightX, $startY, $tubeWidth, $tubeHeight)
    $rightPath = New-Object System.Drawing.Drawing2D.GraphicsPath
    $rightPath.AddArc($rightRect.X, $rightRect.Y, $diameter, $diameter, 180, 90)
    $rightPath.AddArc($rightRect.Right - $diameter, $rightRect.Y, $diameter, $diameter, 270, 90)
    $rightPath.AddArc($rightRect.Right - $diameter, $rightRect.Bottom - $diameter, $diameter, $diameter, 0, 90)
    $rightPath.AddArc($rightRect.X, $rightRect.Bottom - $diameter, $diameter, $diameter, 90, 90)
    $rightPath.CloseFigure()

    # Fill tubes with orange
    $orangeBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 107, 53))
    $graphics.FillPath($orangeBrush, $leftPath)
    $graphics.FillPath($orangeBrush, $rightPath)

    # Add white eyepiece rings at the top
    $whiteBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::White)
    $graphics.FillRectangle($whiteBrush, $startX, $startY, $tubeWidth, $eyepieceHeight)
    $graphics.FillRectangle($whiteBrush, $rightX, $startY, $tubeWidth, $eyepieceHeight)

    # Add white objective rings at the bottom
    $graphics.FillRectangle($whiteBrush, $startX, $bottomY, $tubeWidth, $eyepieceHeight)
    $graphics.FillRectangle($whiteBrush, $rightX, $bottomY, $tubeWidth, $eyepieceHeight)

    $orangeBrush.Dispose()
    $whiteBrush.Dispose()
    $leftPath.Dispose()
    $rightPath.Dispose()

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
