"""Simulation settings."""

from copy import deepcopy

import numpy as np

###################################################################################################
## Define general simulation settings

# Set the number of instances to run (within method simulations)
N_SIMS = 50
N_SIMS2 = 10

# Set the number of samples to run (between method comparisons)
N_SAMPLES = 1000

# General simulation settings
N_SECONDS = 30
FS = 250
FS2 = 500

###################################################################################################
## Define default parameter values

# Define aperiodic parameters
EXP = -1
EXP1 = 0
EXP2 = -2
KNEE = 100

# Define additional parameters related to aperiodic components
F_RANGE = (0.5, None)

# Define periodic parameters
FREQ = 10
BW = 1.5
HEIGHT = 1.5

# Define parameters for combined signals
COMP_VARS = [1, 0.5]

###################################################################################################
## Define parameter ranges

# Aperiodic parameters - ranges
EXPS = np.arange(-3, 0.5, 0.5)
TSCALES = np.array([0.005, 0.015, 0.030, 0.050, 0.075])

KNEES = [25, 100, 400, 900, 1600]

# Periodic parameter - ranges
FREQS = np.arange(5, 36, 1)
POWERS = np.arange(0, 2.1, 0.1)
CVARS = [[1, val] for val in POWERS]
BWS = np.arange(0.5, 3.5, 0.5)

# Burst related parameters
BPROBS = np.arange(0.2, 0.8, 0.1)
