@echo off

:: check for Docker installation
where docker >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
  echo Error: Docker must be installed on your system.
  echo Installation instructions can be found at https://docs.docker.com\engine\install
  exit /B
)

:: check if Docker is running
set "exe=Docker Desktop.exe"
tasklist /fi "imagename eq %exe%" |find ":" > nul
if not errorlevel 1 (
  echo Error: Docker Desktop must be running.
  exit /B
)

:: download data from zenodo
call .\download_data.bat %~1

:: build docker image
call .\build_docker.bat

:: run docker image (automatically executes plot_all.py)
call .\run_docker.bat