@echo off

SET record_id=5748242

echo "Downloading data from Zenodo"
echo ============================
python scripts\download_data.py %record_id%
tar -xzvf pycsep_esrl_data.tar.gz

mkdir figures
echo ""
echo "Building Docker image"
echo =========================
docker build -t pycsep_esrl .

echo ""
echo "Starting Docker container"
echo =========================
echo ""
docker run -it --rm^
 --mount type=bind,source="%cd%"\figures,target=/app/figures^
 --mount type=bind,source="%cd%"\data,target=/app/data,readonly^
 --mount type=bind,source="%cd%"\forecasts,target=/app/forecasts,readonly^
 pycsep_esrl bash
REM Alternatively:
REM docker run -it --rm^
REM  -v "%cd%"\figures:/app/figures -v "%cd%"\data:/app/data -v "%cd%"\forecasts:/app/forecasts^
REM  pycsep_esrl bash