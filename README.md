# Aperiodic Methods

`AperiodicMethods` project repository: characterizing methods for measuring aperiodic neural activity.

[![Website](https://img.shields.io/badge/site-aperiodicmethods.github.io-informational.svg)](https://aperiodicmethods.github.io)

## Overview

Through the history of examining neuro-electrophysiological activity, multiple different approaches
have been employed for measuring patterns of (ir)regularity, (un)predictability, or (a)periodicity.

This project systematically collect and compare approaches for investigating aperiodic activity
(broadly construed) in neuro-electrophysiological recordings, seeking to understand the relationship
between the methods, and to evaluate to what extent they measure different aspects of the data.

Goal(s):
- To test various methods for estimating aperiodic activity
- To determine, empirically, how different methods relate to each other
- To demonstrate these methods on example empirical data

The methods examined in this project include:
- Auto-correlation measures, for investigating the history dependence of time series
- Fluctuation analyses, including the Hurst exponent and detrended fluctuation analysis
- Fractal dimension measures, which characterize fractal properties of time series
- Complexity measures, for estimating signal complexity in neural time series
- Entropy measures, for measuring various entropy measures in time series
- Spectral fitting measures, for measuring aperiodic properties in the frequency domain

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
- [bootstrap](https://github.com/TomDonoghue/bootstrap) >= 0.2.0, used for bootstrapping correlation measures

The full set of requirements is listed in the `requirements.txt` file.

## Repository Layout

This project repository is set up in the following way:

- `apm/` is a custom module that implements code for running this project
- `notebooks/` is a collection of Jupyter notebooks that step through the project
- `scripts/` is a set of Python scripts that run parts of the project
