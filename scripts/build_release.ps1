param(
    [string]$Version = "",
    [string]$Python = ".\.venv\Scripts\python.exe",
    [switch]$NoDictionary
)

$ErrorActionPreference = "Stop"

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $RepoRoot

if (-not (Test-Path $Python)) {
    throw "Python executable not found: $Python. Create the venv first, or pass -Python <path>."
}

if ([string]::IsNullOrWhiteSpace($Version)) {
    $VersionMatch = Get-Content "src\hudict\__init__.py" |
        Select-String -Pattern '__version__\s*=\s*["'']([^"'']+)["'']' |
        Select-Object -First 1
    if (-not $VersionMatch) {
        throw "Could not read HUDict version from src\hudict\__init__.py."
    }
    $Version = $VersionMatch.Matches[0].Groups[1].Value
}

$PyInstaller = Join-Path (Split-Path $Python -Parent) "pyinstaller.exe"
if (-not (Test-Path $PyInstaller)) {
    Write-Host "Installing PyInstaller..."
    & $Python -m pip install pyinstaller
}

if (-not (Test-Path "config.ini")) {
    throw "config.ini is missing. Run HUDict once or create config.ini before building a release."
}

if (-not $NoDictionary -and -not (Test-Path "dictionary.pkl")) {
    throw "dictionary.pkl is missing. Build it first, or pass -NoDictionary to create a source-only release."
}

$ReleaseName = "HUDict-v$Version-windows-x64"
$PyInstallerDist = Join-Path "dist" "pyinstaller"
$PyInstallerBuild = Join-Path "build" "pyinstaller"
$StageDir = Join-Path "dist" $ReleaseName
$ZipPath = Join-Path "dist" "$ReleaseName.zip"

foreach ($Path in @($PyInstallerDist, $PyInstallerBuild, $StageDir, $ZipPath)) {
    if (Test-Path $Path) {
        Remove-Item -LiteralPath $Path -Recurse -Force
    }
}

& $PyInstaller `
    --noconfirm `
    --clean `
    --windowed `
    --noupx `
    --name HUDict `
    --paths src `
    --distpath $PyInstallerDist `
    --workpath $PyInstallerBuild `
    --specpath $PyInstallerBuild `
    --collect-all winsdk `
    src\hudict\app.py

New-Item -ItemType Directory -Path $StageDir | Out-Null
Copy-Item -Path (Join-Path $PyInstallerDist "HUDict\*") -Destination $StageDir -Recurse

Copy-Item -Path "config.ini" -Destination $StageDir
Copy-Item -Path "run-hudict.bat" -Destination $StageDir
Copy-Item -Path "README.md" -Destination $StageDir
Copy-Item -Path "README.zh-CN.md" -Destination $StageDir
if (Test-Path "demo.mp4") {
    Copy-Item -Path "demo.mp4" -Destination $StageDir
}
if (-not $NoDictionary) {
    Copy-Item -Path "dictionary.pkl" -Destination $StageDir
}

Compress-Archive -Path (Join-Path $StageDir "*") -DestinationPath $ZipPath -Force

Write-Host ""
Write-Host "Release package created:"
Write-Host "  $ZipPath"
