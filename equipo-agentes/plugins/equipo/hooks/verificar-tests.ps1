# Stop hook (plugin equipo): no deja terminar el turno con tests rojos.
# Corre pytest solo si: es repo git, hay tests/, hay .py cambiados sin commit,
# y esos cambios no son los mismos de la ultima corrida verde.
$ErrorActionPreference = 'SilentlyContinue'
[Console]::OutputEncoding = [Text.Encoding]::UTF8
$in = [Console]::In.ReadToEnd() | ConvertFrom-Json
if ($in.stop_hook_active) { exit 0 }
$cwd = if ($in.cwd) { $in.cwd } else { (Get-Location).Path }
if (-not (Test-Path $cwd)) { exit 0 }
Set-Location $cwd

$root = git rev-parse --show-toplevel 2>$null
if ($LASTEXITCODE -ne 0 -or -not $root) { exit 0 }
$root = $root -replace '/', '\'
if (-not (Test-Path (Join-Path $root 'tests'))) { exit 0 }

Set-Location $root
$cambios = git status --porcelain --untracked-files=all -- '*.py'
if (-not $cambios) { exit 0 }

$py = @('venv', '.venv') | ForEach-Object { Join-Path $root "$_\Scripts\python.exe" } | Where-Object { Test-Path $_ } | Select-Object -First 1
if (-not $py) { exit 0 }

# Firma del estado actual de los .py: si ya paso en verde, no repetir.
$sha = [Security.Cryptography.SHA1]::Create()
$huella = ($cambios + (git diff -- '*.py') + (git ls-files --others --exclude-standard -- '*.py' | ForEach-Object { Get-Content -Raw $_ })) -join "`n"
$firma = [BitConverter]::ToString($sha.ComputeHash([Text.Encoding]::UTF8.GetBytes($huella))) -replace '-', ''
$idRepo = [BitConverter]::ToString($sha.ComputeHash([Text.Encoding]::UTF8.GetBytes($root))) -replace '-', ''
$marca = Join-Path $env:TEMP "claude-equipo-tests-$idRepo.ok"
if ((Test-Path $marca) -and ((Get-Content -Raw $marca).Trim() -eq $firma)) { exit 0 }

$salida = & $py -m pytest -q -x -p no:cacheprovider 2>&1 | Out-String
$codigo = $LASTEXITCODE
# 0 = verde, 5 = no se recolectaron tests
if ($codigo -eq 0 -or $codigo -eq 5) {
    Set-Content -Path $marca -Value $firma -Encoding ASCII
    exit 0
}
$cola = $salida.Substring([Math]::Max(0, $salida.Length - 2500))
@{ decision = 'block'; reason = "Los tests fallan (pytest exit $codigo). Corrige la causa antes de terminar; no edites los tests para que pasen salvo que el test este mal y lo expliques.`n`n$cola" } | ConvertTo-Json -Compress
exit 0
