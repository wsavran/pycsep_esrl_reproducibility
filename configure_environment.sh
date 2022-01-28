#!/bin/bash
set -e

# check for Docker installation
if [ ! $(command -v docker) ] &> /dev/null
then
    echo "Error: Docker must be installed on your system. Installation instructions can be found at https://docs.docker.com/engine/install/"
    exit /b
fi

# download data from zenodo
./download_data.sh $1
mkdir -p figures
mkdir -p results


# build docker image
./build_docker.sh

# start docker image with bash shell
./start_docker.sh

