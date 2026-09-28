param(
    [string]$ArchifyRoot = "",
    [string]$ArchifyRef = "main"
)

$ErrorActionPreference = "Stop"

if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    throw "Node.js is required. Archify currently requires Node.js 18 or later."
}

if (-not $ArchifyRoot) {
    $toolsRoot = Join-Path $env:LOCALAPPDATA "AgenticLearning"
    $ArchifyRoot = Join-Path $toolsRoot "archify"

    if (-not (Test-Path $ArchifyRoot)) {
        New-Item -ItemType Directory -Force -Path $toolsRoot | Out-Null
        Write-Host "Cloning Archify into $ArchifyRoot"
        git clone --depth 1 --branch $ArchifyRef https://github.com/tt-a1i/archify.git $ArchifyRoot
        if ($LASTEXITCODE -ne 0) {
            throw "Could not clone Archify."
        }
    }
}

$cli = Join-Path $ArchifyRoot "archify\bin\archify.mjs"
$checker = Join-Path $ArchifyRoot "archify\scripts\check-render-output.mjs"

if (-not (Test-Path $cli)) {
    throw "Archify CLI was not found at $cli. Pass -ArchifyRoot pointing to the tt-a1i/archify repository root."
}

Write-Host "Checking Archify runtime..."
node $cli doctor
if ($LASTEXITCODE -ne 0) {
    throw "Archify doctor failed."
}

$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$sourceDir = Join-Path $here "sources"

$jobs = @(
    @{ Source = "01-message-roles.workflow.json"; Output = "roles.html" },
    @{ Source = "02-string-vs-explicit.workflow.json"; Output = "string-vs-explicit.html" },
    @{ Source = "03-conversation-history.workflow.json"; Output = "history.html" },
    @{ Source = "04-history-vs-isolated.workflow.json"; Output = "history-vs-isolated.html" },
    @{ Source = "05-unbounded-history-risks.workflow.json"; Output = "history-risks.html" }
)

$failures = @()
$successes = @()

foreach ($job in $jobs) {
    $inputPath = Join-Path $sourceDir $job.Source
    $outputPath = Join-Path $here $job.Output

    Write-Host ""
    Write-Host "Rendering $($job.Source) -> $($job.Output)"

    node $cli deliver workflow $inputPath $outputPath --quality showcase --json

    if ($LASTEXITCODE -ne 0) {
        $failures += "$($job.Source) (deliver)"
        Write-Warning "Archify deliver failed for $($job.Source). Continuing so all diagram diagnostics are visible."
        continue
    }

    if (Test-Path $checker) {
        node $checker $outputPath

        if ($LASTEXITCODE -ne 0) {
            $failures += "$($job.Output) (artifact check)"
            Write-Warning "Archify output check failed for $($job.Output). Continuing."
            continue
        }
    }

    $successes += $job.Output
}

Write-Host ""
Write-Host "Render summary"
Write-Host "--------------"

if ($successes.Count -gt 0) {
    Write-Host "Succeeded:"
    foreach ($item in $successes) {
        Write-Host " - $item"
    }
}

if ($failures.Count -gt 0) {
    Write-Host ""
    Write-Host "Failed:"
    foreach ($item in $failures) {
        Write-Host " - $item"
    }

    throw "$($failures.Count) Archify diagram(s) failed. Review the diagnostics printed above."
}

Write-Host ""
Write-Host "All five Archify HTML diagrams rendered and passed the artifact check."
