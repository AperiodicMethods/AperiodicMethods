# Aperiodic Methods Notebooks

Welcome to the Aperiodic Methods notebooks!

The notebooks in this project are organized as follows:

## 0) Overview & Background

This section covers an overview and the background for the project, and covers Figures 1 & 2 of the paper.

#### 00-Overview

A general introduction to and overview of the project

#### 01-Outline

An outline of the types of methods included in the project.

#### 02-LiteratureSearch

An examination of the prevalence of these methods in the literature.

## 1) Simulations

Introduces and overviews the simulations used throughout the project.

#### 10-Simulations

Introduction to simulations used in this project.

#### 11-TimeDomainSimulations

Demonstrates examples of time domain simulations across different parameters.

#### 12-TimeSimsParameters

Demonstrates how parameters are managed, iterated across, and sampled from, for time domain simulations.

#### 13-SimulationTests

Overview of how the method evaluation simulations are done.

#### 14-SimulationComparisons

Overview of how the method comparisons simulations are done.

#### 15-PowerSpectrumSimulations

Demonstrates examples of frequency domain simulations across different parameters.

## 2) Time Domain Methods

This section introduces time domain methods, evaluating them on simulated data, and covers Figure 4 of the paper.

#### 20-TimeDomainMethods

Introduction to the time domain methods used in this project.

#### 21-AutoCorrelation

This notebook examines auto-correlation measures.

#### 22-Fluctuations

This notebook examines 'fluctuation' analyses, including the Hurst exponent, and detrended fluctuation analysis (DFA).

#### 23-FractalDimension

This notebook examines fractal dimension measures that can be applied to time series.

#### 24-Complexity

This notebook examines complexity measures that can be applied to time series.

#### 25-Entropy

This notebook examines information theory / entropy measures.

#### 26-MultiscaleEntropy

This notebook examines multiscale entropy measures.

## 3) Spectral Domain Methods

This section introduces spectral domain methods, evaluating and comparing them on simulated data, and covers Figure 3 of the paper.

#### 30-SpectralMethods

Introduction to the spectral domain methods used in this project.

#### 31-SpectralFitting

This notebook examines methods that fit aperiodic components to power spectra.

#### 32-SpecParam

This notebook examines the spectral parameterization ('specparam') method for parameterizing periodic and aperiodic components from neural power spectra.

#### 33-IRASA

This notebook examines the 'irregular resampling auto-spectral analysis' (IRASA) method for decomposing time series.

#### 34-ExponentComparisons

This notebook compares methods that can be used to measure the aperiodic exponent, including specparam and IRASA.

## 4) Method Comparisons

This section compares between the different methods, comparing their results on simulated data, and covers Figure 5 of the paper.

#### 40-MethodComparisons

This notebook introduces how the method comparison simulations are done.

#### 41-WithinComparisons

This notebook compares methods within the different method types, comparing, for example, different complexity measures to each other.

#### 42-BetweenComparisons

This notebook compares methods across different methods types, including testing different types of time domain methods to each other, and comparing time domain methods to frequency domain methods.

## 5) Empirical Comparisons

This section applies and compares the methods on empirical data, and convers Figures 6 & 7 of the paper.

#### 50-DataComparisons

This notebook introduces how the real data are analyzed.

#### 51-EEGData

This notebook introduces real data analysis by analyzing a sample of resting state EEG data.

#### 52-DevelopmentalEEGData

This notebook analyses a larger dataset of developmental EEG data.

#### 53-iEEGData

This notebook examines a dataset of iEEG data.
