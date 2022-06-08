# Reproducing pyCSEP: A Software Toolkit for Earthquake Forecast Developers

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5777992.svg)](https://doi.org/10.5281/zenodo.5777992)

A reproducibility package contains the code and data products needed to recreate the figures from a published article (Krafczyk
et al., 2021). This reproducibility package is meant to provide an introduction to pyCSEP and act as an example on how to create
similar reproducibility packages for future publications. We refer readers interested in creating their own reproducibility packages to
Krafczyk et al. (2021).

We provide the user with options to download a _'full'_ or _'lightweight'_ version of the reproducibility package from Zenodo (see DOI link at the top).
The _'full'_ version of the reproducibility package will recreate Figs. 2‒7 from the manuscript. The _'lightweight'_ version omits
Fig. 3 and Fig. 5 because they require a ~24Gb download for the UCERF3-ETAS forecast, which can take a while (~3h) depending on
the connection to Zenodo. Additionally, these figures require the longest time to create (see [Computational effort](#computational-effort)).

We recommend that users begin with the _'lightweight'_ version of the package for a quick introduction to pyCSEP and to use the
_'full'_ version to learn about evaluating catalog based forecasts. The package is configured to provide turn-key reproducibility
of published results. Users also have granular control if they decide to plot individual figures.

Table of contents
=================

* [Instructions for running](#instructions-for-running)
   * [Prepare the computational environment](#prepare-the-computational-environment)
      * [Easy-mode using Docker](#easy-mode-using-docker)
      * [Using conda environment](#using-conda-environment)
   * [Run the computational environment](#run-the-computational-environment)
      * [Create all figures](#create-all-figures)
      * [Generate individual figures](#generate-individual-figures)
* [Code description](#code-description)
* [Software versions](#software-versions)
* [Computational effort](#computational-effort)
* [References](#references)


## Instructions for running

First, open a terminal and download the reproducibility package from github with
```
git clone https://github.com/wsavran/pycsep_esrl_reproducibility.git
```

Navigate to the newly downloaded directory
```
cd pycsep_esrl_reproducibility
```

### Prepare the computational environment

Now you have two options how to run the package:
 * [Easy-mode using Docker](#easy-mode-using-docker)
 * [Using conda environment](#using-conda-environment)

The easiest way to run the reproducibility package is to run the _'lightweight'_ version of the package in an environment provided
by Docker. If you are interested in working with pyCSEP in more detail or running the _'full'_ version of the reproducibility package,
we recommend that you install pyCSEP (v0.5.2) in a `conda` environment in the native OS.

For both options we have accompanying scripts that work both under Linux/macOS or Windows.

#### Easy mode using Docker

You will need to have the Docker runtime environment installed and running on your machine. Some instructions
can be found [here](https://docs.docker.com/engine/install/). The following commands will not work unless the Docker engine
is correctly installed on your machine.

If on Linux/maxOS, call:
```
./configure_environment.sh
```
If on Windows, call:
```
.\configure_environment.bat
```

This step does the following things: (1) download and verify the checksum of the downloaded
data; (2) build a docker image with the computational environment; and (3) launch the Docker container.


> Note: For best performance on Windows 10/11, Docker should be used with the WSL2 backend instead
of the legacy Hyper-V backend---provided your hardware supports it. This can be configured in
Docker's Settings > General > 'Use the WSL 2 based engine'. For more information and how to enable the WSL2 feature
on your Windows 10/11, see [Docker Desktop WSL 2 backend](https://docs.docker.com/desktop/windows/wsl).

> Note: to download the _'full'_ version, call:
> ```
> ./configure_environment.sh --full
> ```
> or (if on Windows):
> ```
> .\configure_environment.bat --full
> ```

When finished, Docker launches a new shell within the Docker container.
Continue with [Run the computational environment](#run-the-computational-environment).

#### Using conda environment

Installation instructions can be found in the [pyCSEP documentation](https://docs.cseptesting.org/getting_started/installing.html).

Create and activate a new conda environment
```
conda env create -n pycsep_esrl
conda activate pycsep_esrl
```

Install v0.5.2 of pyCSEP
```
conda install --channel conda-forge pycsep=0.5.2
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

### Run the computational environment

The scripts to reproduce the figures in the manuscript are contained in the `scripts` directory; navigate to it using
```
cd scripts
```

> Note: Any script must be launched from the `scripts` directory of the reproducibility package.

#### Create all figures

To produce all figures from the manuscript that are supported by your downloaded version (_'lightweight'_ or _'full'_), run:
```
python plot_all.py
```

Once completed, the figures can be found in the `figures` directory in the top-level directory and results in the `results` directory. These can be
compared against the expected results that are found in the `expected_results` directory.

#### Generate individual figures

Individual scripts can be run by replacing `plot_all.py` above with the name of the script you would like to run (e.g., `plot_figure2.py`).
If you only downloaded the _'lightweight'_ version from Zenodo, you will be unable to run `plot_figure3.py` or `plot_figure5.py`.

If data are already downloaded, figures can be run individually by starting the Docker image and executing scripts manually.
Here is an example to recreate Fig. 2 from the manuscript. The commands should be issued from the `pycsep_esrl_reproducibility`
directory.

```
python plot_figure2.py
```

## Code description

The code to execute the main experiment can be found in the `scripts` directory of this repository. The files are named
according to the figure they create in the manuscript. The script `plot_all.py` will generate all of the figures.
Descriptions of the files in the `scripts` directory are as follows:

* `plot_all.py`: generates all figures listed below
* `plot_figure2.py`: plots RELM and Italian time-independent forecasts with the catalog used to evaluate the forecasts
* `plot_figure3.py`: plots selected catalogs from UCERF3-ETAS forecast
* `plot_figure4.py`: plots S-test and N-test evaluations for RELM and Italian time-independent forecasts
* `plot_figure5.py`: plots S-test and N-test evaluations for UCERF3-ETAS forecasts
* `plot_figure6.py`: plots t-test and W-test evaluations for RELM and Italian time-independent forecasts
* `plot_figure7.py`: illustrates plotting capabilities and manipulation of gridded forecasts
* `experiment_utilities.py`: functions and configuration needed to run the above scripts
* `download_data.py`: downloads data from Zenodo (see DOI link at the top)

## Software versions
* `python>=3.7` 
* `pycsep=0.5.2`

## Computational effort

On a recent (2021) laptop with a 4.6GHz Intel i7, the total runtimes on Windows were as follows:
 * _'lightweight'_ version in Docker and native OS: ~2min
 * _'full'_ version:
   * in Docker: ~1h 40min (~3h on a late 2017 MacBook Pro with a 2.9GHz Intel i7)
   * in native OS: ~1h 5min

The Docker environment introduces latency with I/O operations (only noticible when reading the catalog-based UCERF3-ETAS forecast file).
For optimal performance, we recommend to [use the conda environment](#using-conda-environment).


## References

Krafczyk, M. S., Shi, A., Bhaskar, A., Marinov, D., and Stodden, V. (2021).
Learning from reproducing computational results: introducing three principles and the reproduction package.
_Philosophical Transactions of the Royal Society A: Mathematical, Physical and Engineering Sciences, 379_(2197).
doi: [10.1098/rsta.2020.0069](https://doi.org/10.1098/rsta.2020.0069)
