#!/bin/bash
set -e

# check for Docker installation
if [ ! $(command -v docker) ] &> /dev/null
then
    echo "Error: Docker must be installed on your system. Installation instructions can be found at https://docs.docker.com/engine/install/"
    exit /b
fi

# create necessary folders for the experiment
mkdir -p figures
mkdir -p results

# download data from zenodo
./download_data.sh $1

# build docker image
./build_docker.sh

# run docker image (automatically executes plot_all.py)
./run_docker.sh

