<#
.SYNOPSIS
    Packages a skill into dist/ as a .skill archive, a .zip twin, and a checksum manifest.

.DESCRIPTION
    SPDX-License-Identifier: Apache-2.0
    Copyright 2026 Raul J. Soto

    Produces the release assets described in CLAUDE.md:

        dist/<skill-name>.skill      the primary asset; a plain zip whose single
                                     top-level folder matches the skill's YAML name
        dist/<skill-name>.zip        an identical archive for surfaces that want .zip
        dist/MANIFEST.sha256         per-file checksums, so a truncated-but-present
                                     file fails the gate rather than shipping

    Asset filenames are deliberately unversioned. The version lives in the git
    tag, the release title, and the SKILL.md frontmatter.

    Runs validate-repo.py first by default. Do not skip it to "just get a build
    out" -- the validator is what keeps a malformed skill from being published.

.PARAMETER Skill
    Name of one skill to package, matching its directory under skills/.

.PARAMETER All
    Package every skill.

.PARAMETER SkipValidation
    Skip the conformance check. For local iteration only, never for a release.

.EXAMPLE
    pwsh -File scripts/build-skill.ps1 -Skill deep-analysis

.EXAMPLE
    pwsh -File scripts/build-skill.ps1 -All
#>
[CmdletBinding(DefaultParameterSetName = 'Single')]
param(
    [Parameter(Mandatory, ParameterSetName = 'Single', Position = 0)]
    [string]$Skill,

    [Parameter(Mandatory, ParameterSetName = 'All')]
    [switch]$All,

    [switch]$SkipValidation
)

$ErrorActionPreference = 'Stop'

$repo      = Split-Path -Parent $PSScriptRoot
$skillsDir = Join-Path $repo 'skills'
$distDir   = Join-Path $repo 'dist'

if (-not $SkipValidation) {
    Write-Host 'Validating repository...' -ForegroundColor Cyan
    & python (Join-Path $PSScriptRoot 'validate-repo.py')
    if ($LASTEXITCODE -ne 0) {
        throw 'Validation failed. Fix the reported failures before building; see CLAUDE.md.'
    }
}

$targets = if ($All) {
    Get-ChildItem -Path $skillsDir -Directory | Select-Object -ExpandProperty Name
} else {
    if (-not (Test-Path (Join-Path $skillsDir $Skill))) {
        $available = (Get-ChildItem -Path $skillsDir -Directory | Select-Object -ExpandProperty Name) -join ', '
        throw "No skill named '$Skill'. Available: $available"
    }
    @($Skill)
}

if (-not (Test-Path $distDir)) { New-Item -ItemType Directory -Path $distDir | Out-Null }

$manifestLines = [System.Collections.Generic.List[string]]::new()

foreach ($name in $targets) {
    $sourceDir = Join-Path $skillsDir $name
    $zipPath   = Join-Path $distDir "$name.zip"
    $skillPath = Join-Path $distDir "$name.skill"

    # Read the declared version for the build log. The validator has already
    # confirmed it is present and well-formed.
    $version = (Select-String -Path (Join-Path $sourceDir 'SKILL.md') -Pattern '^version:\s*(.+)$' |
                Select-Object -First 1).Matches.Groups[1].Value.Trim()

    Write-Host "Packaging $name $version" -ForegroundColor Green

    Remove-Item -Path $zipPath, $skillPath -Force -ErrorAction SilentlyContinue

    # Compressing the directory itself yields an archive whose single top-level
    # folder is the directory name. The validator guarantees that equals the
    # YAML name, which is what the install surfaces key on.
    Compress-Archive -Path $sourceDir -DestinationPath $zipPath -CompressionLevel Optimal
    Copy-Item -Path $zipPath -Destination $skillPath

    foreach ($file in Get-ChildItem -Path $sourceDir -Recurse -File | Sort-Object FullName) {
        $relative = [IO.Path]::GetRelativePath($skillsDir, $file.FullName).Replace('\', '/')
        $hash     = (Get-FileHash -Path $file.FullName -Algorithm SHA256).Hash.ToLower()
        $manifestLines.Add("$hash  $relative")
    }

    foreach ($asset in @($skillPath, $zipPath)) {
        $hash = (Get-FileHash -Path $asset -Algorithm SHA256).Hash.ToLower()
        $manifestLines.Add("$hash  dist/$(Split-Path -Leaf $asset)")
    }

    $sizeKb = [math]::Round((Get-Item $skillPath).Length / 1KB, 1)
    Write-Host "  dist/$name.skill  ($sizeKb KB)"
    Write-Host "  dist/$name.zip"
}

$manifestPath = Join-Path $distDir 'MANIFEST.sha256'
Set-Content -Path $manifestPath -Value $manifestLines -Encoding utf8NoBOM
Write-Host "  dist/MANIFEST.sha256 ($($manifestLines.Count) entries)"

Write-Host ''
Write-Host 'Build complete. To release (tag and title carry the version, the asset does not):' -ForegroundColor Cyan
foreach ($name in $targets) {
    $version = (Select-String -Path (Join-Path $skillsDir $name 'SKILL.md') -Pattern '^version:\s*(.+)$' |
                Select-Object -First 1).Matches.Groups[1].Value.Trim()
    Write-Host "  git tag $name-v$version && git push origin $name-v$version"
    Write-Host "  gh release create $name-v$version --title `"$name v$version`" dist/$name.skill dist/$name.zip dist/MANIFEST.sha256"
}
Write-Host ''
Write-Host 'Then update the README skill index: version column and download link.' -ForegroundColor Yellow
