#! /bin/bash

echo ''
echo 'Launching Docker container'
echo '=========================='
docker run -it --rm \
--mount type=bind,source="$(pwd)"/figures,target=/app/figures \
--mount type=bind,source="$(pwd)"/results,target=/app/results \
--mount type=bind,source="$(pwd)"/data,target=/app/data,readonly \
--mount type=bind,source="$(pwd)"/forecasts,target=/app/forecasts,readonly \
pycsep_esrl bash && cd scripts
