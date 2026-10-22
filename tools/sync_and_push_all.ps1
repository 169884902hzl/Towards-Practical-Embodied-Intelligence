#Requires -Version 5.1
<#
.SYNOPSIS
    Inspect this repository and optionally push existing commits.
    Never stages, commits, force-pushes, or visits another repository.
#>
param([switch]$Push)
$ErrorActionPreference = "Stop"
$Repo = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Push-Location $Repo
try {
    git --no-optional-locks status --short --branch
    if ($LASTEXITCODE -ne 0) { throw "Unable to inspect repository" }
    git log --oneline '@{upstream}..HEAD'
    if ($LASTEXITCODE -ne 0) { throw "Configure an upstream before pushing" }
    if ($Push) {
        $dirty = git --no-optional-locks status --porcelain
        if ($dirty) { throw "Review and commit working changes explicitly before using -Push" }
        git push
        if ($LASTEXITCODE -ne 0) { throw "Push failed" }
    }
} finally {
    Pop-Location
}
