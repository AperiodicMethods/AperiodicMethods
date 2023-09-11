"""Default settings file."""

import numpy as np

###################################################################################################
###################################################################################################

# Set the number of instances to run
N_SIMS = 50

# General simulation settings
N_SECONDS = 30
FS = 500

# Define aperiodic parameters
EXP = -1.5
KNEE =

# Define additional parameters related to aperiodic components
F_RANGE = (0.5, None)

# Define periodic parameters
FREQ = 10
BW = 1.5
HEIGHT = 1.5

# Define parameters for combined signals
COMP_VARS = [1, 0.25]

# Aperiodic parameters - ranges
EXPS = np.arange(-3, 0.5, 0.5)
KNEES = np.array([0.002, 0.005, 0.015, 0.040, 0.070])

# Periodic parameter - ranges
FREQS = np.arange(1, 50, 2)
POWERS = np.arange(0, 2, 0.1)
BWS = np.arange(0, 2.0, 0.5)

# Collect together simulation parameters
SIM_PARAMS_AP = {'n_seconds' : N_SECONDS, 'fs' : FS, 'f_range' : F_RANGE}
SIM_PARAMS_KNEE = {'n_seconds' : N_SECONDS, 'fs' : FS}
SIM_PARAMS_COMB = {'n_seconds' : N_SECONDS, 'fs' : FS,
                   'components' : {'sim_powerlaw' : {'exponent' : EXP, 'f_range' : F_RANGE},
                                   'sim_oscillation' : {'freq' : FREQ}},
                   'component_variances' : COMP_VARS}
SIM_PARAMS_BURST = {'n_seconds' : N_SECONDS, 'fs' : FS,
                    'components' : {'sim_powerlaw' : {'exponent' : EXP, 'f_range' : F_RANGE},
                                    'sim_bursty_oscillation' : {'freq' : FREQ}},
                    'component_variances' : COMP_VARS}
SIM_PARAMS_PEAK = {'freq' : FREQ, 'bw' : BW, 'height' : HEIGHT}
