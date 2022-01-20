@echo off

SET record_id=5777992

IF "%~1" == -h (
  echo "Usage: %undefined% [-h] [--full]

      where:
         -h        Show help message
         --full    Download all files from reproducibilty package. Default is lightweight version.

      More information available in the README file.
      "
  exit
)
echo.
echo Downloading data from Zenodo
echo ============================
python scripts\download_data.py %record_id% %~1