param(
    [string]$Version = "",
    [switch]$Draft,
    [switch]$Prerelease,
    [switch]$NoDictionary
)

$ErrorActionPreference = "Stop"

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $RepoRoot

if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    throw "GitHub CLI is not installed. Install it from https://cli.github.com/ and run 'gh auth login' first."
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

& (Join-Path $PSScriptRoot "build_release.ps1") -Version $Version -NoDictionary:$NoDictionary

$ReleaseName = "HUDict-v$Version-windows-x64"
$ZipPath = Join-Path "dist" "$ReleaseName.zip"
$Tag = "v$Version"

$GhArgs = @(
    "release", "create", $Tag, $ZipPath,
    "--title", "HUDict $Version",
    "--notes", "Windows release package for HUDict $Version."
)

if ($Draft) {
    $GhArgs += "--draft"
}

if ($Prerelease) {
    $GhArgs += "--prerelease"
}

& gh @GhArgs
