@echo off

echo.
echo Launching Docker container
echo ==========================
docker run -it --rm^
 --mount type=bind,source="%cd%"\figures,target=/app/figures^
 --mount type=bind,source="%cd%"\data,target=/app/data,readonly^
 --mount type=bind,source="%cd%"\forecasts,target=/app/forecasts,readonly^
 pycsep_esrl bash

REM Alternative #1:
REM docker run -it --rm^
REM  -v "%cd%"\figures:/app/figures -v "%cd%"\data:/app/data -v "%cd%"\forecasts:/app/forecasts^
REM  pycsep_esrl bash

REM Alternative #2 (passes command to WSL)
REM wsl docker run -it --rm^
REM  --mount type=bind,source="$(pwd)"/figures,target=/app/figures^
REM  --mount type=bind,source="$(pwd)"/data,target=/app/data,readonly^
REM  --mount type=bind,source="$(pwd)"/forecasts,target=/app/forecasts,readonly^
REM  pycsep_esrl bash