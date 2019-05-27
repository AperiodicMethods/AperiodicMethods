# Aperiodic Methods

Neuro-electrophysiological data is includes aperiodic components, or 1/f-like activity.

There are many possible ways to measure such activity. This project explores those methods.

Goal(s):
- To test various methods for estimating aperiodic activity, including
    - Spectral fitting approaches for measure aperiodic properties in the frequency domain
    - Time series methods for estimating signal complexity and 1/f properties
- To determine, empirically, how different methods relate to each other
- To evaluate which methods are the most accurate, given simualted data

## Dependencies

This project is written in Python3.

Dependencies:
- numpy
- scipy
- pandas
- scikit-learn
- matplotlib
- FOOOF (https://github.com/fooof-tools/fooof)
- NeuroDSP (https://github.com/neurodsp-tools/neurodsp)

## APM

This project includes a custom module, `apm` that implements the 'aperiodic methods' for the project.
