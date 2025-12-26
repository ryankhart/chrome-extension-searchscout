# Package SearchScout extension for Chrome Web Store
# This script creates a ZIP file containing only the runtime files

$extensionName = "SearchScout"
$version = "1.0.0"
$outputFile = "$extensionName-$version.zip"

# Remove old package if it exists
if (Test-Path $outputFile) {
    Remove-Item $outputFile
    Write-Host "Removed old package: $outputFile"
}

# Files and folders to include in the package
$filesToInclude = @(
    "manifest.json",
    "background.js",
    "modules",
    "popup",
    "icons/icon16.png",
    "icons/icon32.png",
    "icons/icon48.png",
    "icons/icon128.png"
)

Write-Host "Creating package: $outputFile"
Write-Host "Including files:"

# Create the ZIP file
Compress-Archive -Path $filesToInclude -DestinationPath $outputFile -Force

foreach ($file in $filesToInclude) {
    Write-Host "  - $file"
}

Write-Host ""
Write-Host "Package created successfully: $outputFile" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:"
Write-Host "1. Upload $outputFile to Chrome Web Store Developer Dashboard"
Write-Host "2. Upload screenshots separately in the store listing interface"
