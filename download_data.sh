#!/bin/bash
set -e

# DO NOT CHANGE THIS
record_id=5777992

# usage information
if [ "$1" == "-h" ]
then
    echo "Usage: `basename $0` [-h] [--full]

    where:
       -h        Show help message
       --full    Download all files from reproducibilty package. Default is lightweight version.

    More information available in the README file.
    "
    exit
fi

echo ''
echo 'Downloading data from Zenodo'
echo '============================'
python ./scripts/download_data.py $record_id $1

mkdir -p figures
mkdir -p results
