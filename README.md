# Aperiodic Methods

`AperiodicMethods` project repository: characterizing methods for measuring aperiodic neural activity.

[![Website](https://img.shields.io/badge/site-aperiodicmethods.github.io-informational.svg)](https://aperiodicmethods.github.io)

## Overview

Neuro-electrophysiological data contains, or 1/f-like, aperiodic activity.

There are many possible ways to measure such activity. This project explores and compares those methods.

Goal(s):
- To test various methods for estimating aperiodic activity
- To determine, empirically, how different methods relate to each other
- To evaluate which methods are the most accurate, given simulated data
- To demonstrate these methods on example empirical data

The methods examined in this project include:
- Spectral fitting approaches for measuring aperiodic properties in the frequency domain, including specparam and IRASA
- Auto-correlation measures for investigating the history dependence of time series
- Fluctuation analyses, including the Hurst exponent and detrended fluctuation analysis
- Fractal dimension measures, which characterize fractal properties of time series
- Methods for estimating signal complexity in neural time series
- Information theory measures for measuring various entropy measures in time series

You can explore this project by looking through the `notebooks`, and/or explore the hosted version on the
[website](https://aperiodicmethods.github.io/).

## Reference

A preprint for this project is upcoming.

## Requirements

This project was written in Python 3 and requires Python >= 3.7 to run.

This project requires external dependencies, including standard scientific packages.

In addition, this project requires the following dependencies:
- [neurodsp](https://github.com/neurodsp-tools/neurodsp) >= 2.3, used for simulating time series and applying methods
- [fooof](https://github.com/fooof-tools/fooof) == 1.1, used for simulating power spectra and applying spectral fits
- [lisc](https://github.com/lisc-tools/lisc) >= 0.3, used for the literature search
- [antropy](https://github.com/raphaelvallat/antropy), used for entropy and complexity measures
- [neurokit2](https://github.com/neuropsychology/NeuroKit), used for some additional complexity measures

The full set of requirements is listed in the `requirements.txt` file.

## Repository Layout

This project repository is set up in the following way:

- `apm/` is a custom module that implements the 'aperiodic methods' for the project
- `notebooks/` is a collection of Jupyter notebooks that step through the project
- `scripts/` is a set of Python scripts that run parts of the project
