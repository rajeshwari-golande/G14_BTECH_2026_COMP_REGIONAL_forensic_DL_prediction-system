@echo off
REM TC25 - Docker build backend (works when PowerShell scripts are blocked)

set "BACK=%~dp0..\deployment\backend"
cd /d "%BACK%"
if not exist Dockerfile (
  echo ERROR: Dockerfile not found in %BACK%
  exit /b 1
)

echo TC25 - Docker build (backend)
echo Context: %CD%

docker build -t forensic-backend-tc25:latest .
set "EC=%ERRORLEVEL%"
if %EC% neq 0 exit /b %EC%
echo PASS (exit 0)
exit /b 0
