# Aperiodic Methods

Project repository for the `AperiodicMethods` project, exploring methods for measuring aperiodic activity in neural data.

## Overview

Neuro-electrophysiological data is includes aperiodic components, or 1/f-like activity.

There are many possible ways to measure such activity. This project explores and compares those methods.

Goal(s):
- To test various methods for estimating aperiodic activity, including
    - Spectral fitting approaches for measure aperiodic properties in the frequency domain
    - Time series methods for estimating signal complexity and 1/f properties
- To determine, empirically, how different methods relate to each other
- To evaluate which methods are the most accurate, given simulated data

## Project Guide

You can follow along with this project by stepping through the whole thing, as outlined in the `notebooks`.

If you want to re-run the whole project, keep in mind that some parts are done by stand-alone scripts, available in the `scripts` folder. These scripts are described by the analysis outline in the notebooks.

## Dependencies

This project was written in Python 3 and requires Python >= 3.7 to run.

If you want to re-run this project, you will need some external dependencies.

Dependencies include 3rd party scientific Python packages:
- [numpy](https://github.com/numpy/numpy)
- [pandas](https://github.com/pandas-dev/pandas)
- [scipy](https://github.com/scipy/scipy)
- [scikit-learn](https://github.com/scikit-learn/scikit-learn)
- [matplotlib](https://github.com/matplotlib/matplotlib)
- [seaborn](https://github.com/mwaskom/seaborn)

You can get and manage these dependencies using the [Anaconda](https://www.anaconda.com/distribution/) distribution, which we recommend.

In addition, this project requires the following dependencies:

 - [fooof](https://github.com/fooof-tools/fooof) >= 1.0.0
 - [neurodsp](https://github.com/neurodsp-tools/neurodsp) >= 2.0.0

You can install the extra required dependencies by running:

```
pip install fooof, neurodsp
```

## Repository Layout

This project repository is set up in the following way:

- `apm/` is a custom module that implements the 'aperiodic methods' for the project
- `data/` contains the simulated data used in the project
- `figures/` holds all figures produced throughout the project
- `notebooks/` is a collection of Jupyter notebooks that step through the project
- `scripts/` contains stand alone scripts that run parts of the project
