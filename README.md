# Reproducing pyCSEP: A Software Toolkit for Earthquake Forecast Developers


## Code description

The code to execute the main experiment can be found in the ```scripts``` directory of this repository. The files are named
according to the figure they create in the manuscript. The script ```plot_all.py``` will generate all of the figures.
Descriptions of the files in the ```scripts``` folder are below:

* plot_figure2.py: plots RELM and Italian time-independent forecasts with the catalog used to evaluate the forecasts
* plot_figure3.py: plots selected catalogs from UCERF3-ETAS forecast
* plot_figure4.py: plots S-test and N-test evaluations for RELM and Italian time-independent forecasts
* plot_figure5.py: plots S-test and N-test evaluations for UCERF3-ETAS forecasts 
* plot_figure6.py: plots t-test and W-test evaluations for RELM and Italian time-independent forecasts
* plot_figure7.py: illustrates plotting capabilities and manipulation of gridded forecasts 
* experiment_utilities.py: functions and configuration needed to run the above scripts
* download_data.py: downloads data from Zenodo (doi: 10.5281/zenodo.5748242)
* plot_all.py: generates all figures listed above

### Software versions
python=3.7.3  
pycsep=0.5.1  
Docker  

## Software dependencies

In order to run this reproducibility package, the user must have access to a Unix shell that has python3 installed with the requests libary. You can install the requests library using

    pip install requests
    
Additionally, you will need to have the Docker runtime environment installed and running on your machine. The computational
envrironment to recreate the figures from the manuscript will be provided by the Docker image.
   

## Instructions for running

Once you have downloaded the reproducibility package from GitHub using 
```
git clone git@github.com:wsavran/pycsep_esrl_reproducibility.git
```

Navigate to the newly downloaded directory
```
cd pycsep_esrl_reproducibility
```

Build the computational enviornment. This step does the following 3 things: (1) downloads and verifies the checksum of the
data; (2) builds a docker image with the computational environemnt; and (3) launches the Docker container to run the plotting
scripts.
```
./build_environment.sh
```

Produce each figure from the manuscript by running the following command in the newly launched shell provided by Docker
```
python scripts/plot_all.py
```

Note: Individual scripts can be run by replacing the script name above with the name of the script you would like to run (e.g.,
scripts/plot_all.py with scripts/plot_figure2.py). 

The Docker environment introduces considerable I/O issues when running on
Windows or MacOS. If you are interested in working with these scripts in more detail, we recommend that you install v0.5.1 of
pyCSEP in a `conda` environment on your personal computer or workstation. Installation instructions can be found in the [pyCSEP
documentation](https://docs.cseptesting.org/getting_started/installing.html).




