# scripts/start.ps1
Set-StrictMode -Version Latest

# Activate venv if present
if (Test-Path .\.venv\Scripts\Activate.ps1) {
    . .\.venv\Scripts\Activate.ps1
}

# load .env into environment (simple)
if (Test-Path .\.env) {
    Get-Content .\.env | ForEach-Object {
        if ($_ -and ($_ -notmatch '^\s*#')) {
            $parts = $_ -split '='
            $k = $parts[0].Trim()
            $v = ($parts[1..($parts.Length-1)] -join "=").Trim()
            [System.Environment]::SetEnvironmentVariable($k, $v)
        }
    }
}

# start mongo via docker-compose
docker compose up -d mongo

# start app
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
