@echo off

docker run -it --rm^
 --mount type=bind,source="%cd%"\figures,target=/app/figures^
 --mount type=bind,source="%cd%"\results,target=/app/results^
 --mount type=bind,source="%cd%"\data,target=/app/data,readonly^
 --mount type=bind,source="%cd%"\forecasts,target=/app/forecasts,readonly^
 --entrypoint /bin/bash^
 pycsep_esrl

REM Alternative #1:
REM docker run -it --rm^
REM  -v "%cd%"\figures:/app/figures -v "%cd%"\results:/app/results -v "%cd%"\data:/app/data -v "%cd%"\forecasts:/app/forecasts^
REM  --entrypoint /bin/bash^
REM  pycsep_esrl bash

REM Alternative #2 (passes command to WSL)
REM wsl docker run -it --rm^
REM  --mount type=bind,source="$(pwd)"/figures,target=/app/figures^
REM  --mount type=bind,source="$(pwd)"/results,target=/app/results^
REM  --mount type=bind,source="$(pwd)"/data,target=/app/data,readonly^
REM  --mount type=bind,source="$(pwd)"/forecasts,target=/app/forecasts,readonly^
REM  --entrypoint /bin/bash^
REM  pycsep_esrl bash
