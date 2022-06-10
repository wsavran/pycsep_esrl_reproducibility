#! /bin/bash --login
set -euo pipefail
conda activate pycsep-env
set +euo pipefail
cd scripts
exec python plot_all.py