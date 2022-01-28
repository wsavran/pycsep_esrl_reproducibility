# Reproducing pyCSEP: A Software Toolkit for Earthquake Forecast Developers

A reproducibility package contains the code and data products needed to recreate the figures from a published article (Krafczyk
et al., 2021). This reproducibility package is meant to provide an introduction to pyCSEP and act as an example on how to create
similar reproducibility packages for future publications. We refer readers interested in creating their own reproducibility packages to 
Krafczyk et al. (2021).

We provide the user with options to download a 'full' or 'lightweight' version of the reproducibility package. The 'full'
version of the reproducibility package will recreate Figs. 2 - 7 from the manuscript. The 'lightweight' version omits
Fig. 3 and Fig. 5. The omitted figures require a ~26Gb download for the UCERF3-ETAS forecast, which can be slow depending on
the connection to Zenodo. Additionally, these figures require the longest time to create. 

We recommend that users begin with the 'lightweight' version of the package for a quick introduction to pyCSEP and to use the 
'full' version to learn about evaluating catalog based forecasts. The package is configured to provide turn-key reproducibility
of published results. Users also have granular control if they decide to plot individual figures.

## Instructions for running

First, download the reproducibility package from Zenodo and navigate to the directory on your computer 

```
git clone git@github.com:wsavran/pycsep_esrl_reproducibility.git
```

Navigate to the newly downloaded directory
```
cd pycsep_esrl_reproducibility
```

### Easy-mode using Docker

The easiest way to run the reproducibility package is to run the 'lightweight' version of the package in an environment provided
by Docker. You will need to have the Docker runtime environment installed and running on your machine. Some instructions
can be found [here](https://docs.docker.com/engine/install).

> Note: For best performance on Windows 10/11, Docker should be used with the WSL2 backend instead
of the legacy Hyper-V backend---provided your hardware supports it. This can be configured in
Docker's Settings > General > 'Use the WSL 2 based engine'. For more information and how to enable the WSL2 feature
on your Windows 10/11, see [Docker Desktop WSL 2 backend](https://docs.docker.com/desktop/windows/wsl).

The following commands will not work unless the Docker engine
is correctly installed on your machine.


#### Build the computational enviornment

If on Linux/maxOS, call:
```
./configure_environment.sh
```
If on Windows, call:
```
.\configure_environment.bat
```

This step does the following things: (1) downloads and verifies the checksum of the downloaded
data; (2) builds a docker image with the correct computational environemnt; and (3) launches the Docker container to run the plotting
scripts.

> Note: to download the _'full'_ version, call:
> ```
> ./configure_environment.sh --full
> ```
> or (if on Windows):
> ```
> .\configure_environment.bat --full
> ```


The scripts to reproduce the figures in the manuscript are contained in the `scripts` folder. Navigate to this folder using
```
cd scripts
```


#### Run main script to create all figures

Produce each figure from the manuscript by running the following command in the newly launched shell provided by Docker
```
python plot_all.py
```

### Generate Individual Figures

Individual scripts can be run by replacing the script name above with the name of the script you would like to run (e.g.,
scripts/plot_all.py with scripts/plot_figure2.py). Scripts should be launched from the top-level directory of the
reproducibility package. You will be unable to run `scripts/plot_figure3.py` or `scripts/plot_figure5.py` if you only
downloaded the 'lightweight' version of the files from Zenodo.

If data are already downloaded, figures can be run individually by starting the Docker image and executing scripts manually. 
Here is an example to recreate Fig. 2 from the manuscript. The commands should be issued from the `pycsep_esrl_reproducibility`
folder.

```
./start_docker.sh
cd scripts
python plot_figure2.py
```

### Using conda environment 

If you are interested in working with pyCSEP in more detail or running the full-version of the reproducibility package, 
we recommend that you install v0.5.1 of pyCSEP in a `conda` environment on your personal computer or workstation. 
Installation instructions can be found in the [pyCSEP documentation](https://docs.cseptesting.org/getting_started/installing.html).

Create and activate conda environment
```
conda env create -n pycsep_v051
conda activate pycsep_v051
```

Install v0.5.1 of pyCSEP
```
conda install --channel conda-forge pycsep=0.5.1
```

Download data from Zenodo
```
./download_data.sh
```
or (if on Windows):
```
.\download_data.bat
```

> Note: to download the _'full'_ version, append ` --full` to the command (see [above](#easy-mode-using-docker))


## Code description

The code to execute the main experiment can be found in the ```scripts``` directory of this repository. The files are named
according to the figure they create in the manuscript. The script ```plot_all.py``` will generate all of the figures.
Descriptions of the files in the ```scripts``` folder are below:

* `plot_all.py`: generates all figures listed below
* `plot_figure2.py`: plots RELM and Italian time-independent forecasts with the catalog used to evaluate the forecasts
* `plot_figure3.py`: plots selected catalogs from UCERF3-ETAS forecast
* `plot_figure4.py`: plots S-test and N-test evaluations for RELM and Italian time-independent forecasts
* `plot_figure5.py`: plots S-test and N-test evaluations for UCERF3-ETAS forecasts 
* `plot_figure6.py`: plots t-test and W-test evaluations for RELM and Italian time-independent forecasts
* `plot_figure7.py`: illustrates plotting capabilities and manipulation of gridded forecasts 
* `experiment_utilities.py`: functions and configuration needed to run the above scripts
* `download_data.py`: downloads data from Zenodo (doi: 10.5281/zenodo.5748242)

### Software versions
`python>=3.7`  
`pycsep=0.5.1`  

## Software dependencies

In order to run this reproducibility package, the user must have access to a Unix shell that has python3 installed with the requests library. 
You can install the requests library using depending on your Python package manager.

```
conda install requests
```
or 
```
pip install requests
```

## References

Krafczyk, M. S., Shi, A., Bhaskar, A., Marinov, D., and Stodden, V. (2021). Learning from reproducing computational results: introducing three principles and the reproduction package. Philosophical Transactions of the Royal Society A: Mathematical, Physical and Engineering Sciences, 379(2197).


