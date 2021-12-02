#!/bin/bash
set -e

record_id=5717419

echo 'Downloading data from Zenodo'
echo '============================'
python ./scripts/download_data.py $record_id 
tar -xzvf pycsep_esrl_data.tar.gz
mkdir -p figures

echo ''
echo 'Building Docker image'
echo '========================='
docker build -t pycsep_esrl .

echo ''
echo 'Starting Docker container'
echo '========================='
echo ''
docker run -it --rm \
--mount type=bind,source="$(pwd)"/figures,target=/app/figures \
--mount type=bind,source="$(pwd)"/data,target=/app/data,readonly \
--mount type=bind,source="$(pwd)"/forecasts,target=/app/forecasts,readonly \
pycsep_esrl bash

