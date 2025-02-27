## Table of contents:

1. Installation
2. Preparing input data
3. Producing results
4. Analyzing results

## Installation:

1. Prepare your data directory.

The data directory contains input files for the projection system, and
generally is where output files are written. The necessary inputs
differ depending on the projection being performed, but generally
consist of projection climate data and socioeconomic data, and common
region definitions.

This directory can be in any accessible location on the computer. Its
location will be used in a later step.

2. Prepare the software environment.

The easiest way to install the necessary libraries is to use a conda
environment, as follows:

From the root directory of this repository, call
```
conda env create -f environment.yml -n env
```

Then activate `env` with `conda activate env` and run
```
pip install -e .
```
to do a "development install" of impact-calculations. When ready, you
can deactivate the environment with `conda deactivate`.

If you need to install custom branches of any of the CIL libraries
(like `open-estimate`), you can run something like the following
(shown for a `new_feature_branch` of `open-estimate`):
```
pip install git+https:github.com/climateimpactlab/open-estimate@new_feature_branch --upgrade
```
which will tell the environment to overwrite and use the
`open-estimate` package installed from that branch.

Alternatively, you can install the necessary libraries by hand. The
remaining text in this section provides information on doing that. If you do this, we recommend that you start by creating a virtual environment to keep python packages separate across projects.

First, make a new virtual environment directory, execuing from your project directory:
```
python -m venv env
```

This will create a directory `env` within the current directory.

Now, activate the virtual environment to "enter" its set of packages:
```
source env/bin/activate
```

Now, all of your `pip` commands will add packages just to the environment.  Drop all `--user` arguments from the `pip` commands below.
You will need to do this last line every time you want to use the system.

Next, install a laundry-list of public packages, if they aren't
already installed (use `--user` for pip commands on a shared
computer):
 - numpy
 - netcdf: `apt-get install python-netcdf netcdf-bin libnetcdfc++4 libnetcdf-dev`.
       You may need to install
       `https://github.com/Unidata/netcdf4-python` from the source
 - libhdf5 and h5py: `apt-get install libhdf5-serial-dev`; `pip install h5py`
 - metacsv: `pip install metacsv`
 - libffi-dev: `apt-get install libffi-dev`
 - statsmodels: `pip install statsmodels`
 - scipy: `apt-get install libblas-dev liblapack-dev gfortran`; `pip install scipy`
 - xarray: `pip install xarray==0.10.9`
 - pandas: `pip install pandas==0.25.3`

Install the custom `open-estimate`, `impactlab-tools` and
`impact-common` libraries.

If you will not be developing code in the projection system, you can
do this directly with `pip`:

 - `open-estimate`: ```$ pip install git+https://github.com/climateimpactlab/open-estimate```
 - `impactlab-tools`: ```$ pip install git+https://github.com/ClimateImpactLab/impactlab-tools.git```
 - `impact-common`: ```$ pip install git+https://github.com/ClimateImpactLab/impact-common.git```

In many cases, however, changes to the projection system functioning
requires changes to these libraries. In this case, it is recommended
that you clone the git repositories and run `pip install -e .` to
install an editable version. Specifically:

Clone `open-estimate` to your project directory:
   ```$ git clone https://github.com/ClimateImpactLab/open-estimate.git```

Install it: 
```
$ cd open-estimate
$ pip install -e .
$ cd ..
```

Similarly, install `impactlab-tools` and `impact-common`:
```
$ git clone https://github.com/ClimateImpactLab/impactlab-tools.git
$ cd impactlab-tools
$ pip install -e .
$ cd ..
$ git clone https://github.com/ClimateImpactLab/impact-common.git
$ cd impact-common
$ pip install -e .
$ cd ..
```

3. Install the `impact-calculations` repository.

Clone `impact-calculations` to your project directory:
   ```$ git clone git@bitbucket.org:ClimateImpactLab/impact-calculations.git```

The `impact-calculations` code needs to know where to find the data
directory from step 1. There are two ways to configure the system.

Option 1: `IMPERICS_SHAREDDIR`:

You can export the environmental variable with the path to the data
directory, as follows:

```
export IMPERICS_SHAREDDIR=<full-path-to-data-directory>
```

You may want to add this line to your `~/.bashrc` file, to export it
any time you start a bash shell.

Option 2: `server.yml`:

You can create a file named `server.yml` in the directory that
contains the `impact-calculations` directory.

The contents of this file should be:
```
shareddir: <full-path-to-data-directory>
```

## Producing results

Diagnostic, median, and Monte Carlo results are produced by calling `./generate.sh CONFIG.yml`.  The `CONFIG.yml` files are stored in the `configs/` directory.  You may optionally put a number after this command, to spawn that many background processes.  Here are example commands:

* Generate a diagnostic collection of predictors and outputs for each region and year:
  ```$ ./generate.sh configs/mortality-diagnostic.yml```

* Generate results for the median quantile of the econometric distributions:
  ```$ ./generate.sh configs/mortality-median.yml```

* Generate results performing a Monte Carlo across econometric uncertainty with 10 processes:
  ```$ ./generate.sh configs/mortality-montecarlo.yml 10```

## Analyzing results

### Timeseries results

* Clone the `prospectus-tools` repository on a machine with results:
  ```$git clone https://github.com/jrising/prospectus-tools.git tools```

* Make any changes to the `tools/gcp/extract/configs/timeseries.yml` file, following the information in the `README.md` and `config-dogs.md` in `tools/gcp/extract`.

* From the `tools/gcp/extract` directory, extract all timeseries available for each RCP and SSP:
  ```$ python quantiles.py configs/timeseries.yml RESULT-PREFIX```
    - `RESULT-PREFIX` is a prefix in the filenames of the `.nc4` result files.  It might be (for example) each of the following:
        - `interpolated_mortality_all_ages-histclim` or `interpolated_mortality_all_ages-histclim-aggregated`: historical climate impacts, non-aggregated and aggregated.
        - `interpolated_mortality_all_ages` or `interpolated_mortality_all_ages-aggregated`: normal full-adaptation impacts
        - `interpolated_mortality_ASSUMPTION_all_ages-aggregated` or `interpolated_mortality_ASSUMPTION_all_ages-aggregated`: partial adaptation, where `ASSUMPTION` is `incadapt` or `noadapt`.
        - `interpolated_mortality_all_ages-costs` or `interpolated_mortality_all_ages-costs-aggregated`: cost estimates (combine with `VARIABLE` optional argument).
