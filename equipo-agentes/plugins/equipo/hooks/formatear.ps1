# PostToolUse hook (plugin equipo): formatea con ruff el .py recien editado.
# No hace nada si el archivo no es .py o si el venv del proyecto no tiene ruff.
$ErrorActionPreference = 'SilentlyContinue'
$in = [Console]::In.ReadToEnd() | ConvertFrom-Json
$archivo = $in.tool_input.file_path
if (-not $archivo -or $archivo -notmatch '\.pyi?$' -or -not (Test-Path $archivo)) { exit 0 }

# Busca venv/.venv subiendo desde la carpeta del archivo.
$dir = Split-Path -Parent (Resolve-Path $archivo).Path
$ruff = $null
while ($dir -and -not $ruff) {
    $ruff = @('venv', '.venv') | ForEach-Object { Join-Path $dir "$_\Scripts\ruff.exe" } | Where-Object { Test-Path $_ } | Select-Object -First 1
    $padre = Split-Path -Parent $dir
    if ($padre -eq $dir) { break }
    $dir = $padre
}
if (-not $ruff) { exit 0 }

& $ruff format --quiet $archivo | Out-Null
& $ruff check --fix --quiet $archivo | Out-Null
exit 0
