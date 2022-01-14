"""Default settings file."""

import numpy as np

###################################################################################################
###################################################################################################

# General simulation settings
N_SECONDS = 30
FS = 1000

EXP = -2
FREQ = 10

COMP_VARS = [1, 0.25]

# Collect together simulation parameters
SIM_PARAMS_AP = {'n_seconds' : N_SECONDS, 'fs' : FS}
SIM_PARAMS_COMB = {'n_seconds' : N_SECONDS, 'fs' : FS,
                   'components' : {'sim_powerlaw' : {'exponent' : EXP},
                                   'sim_oscillation' : {'freq' : FREQ}},
                   'component_variances' : COMP_VARS}

# Set the number of instances to run
N_SIMS = 50

# Set the range of exponents to explore
EXPS = np.arange(-3, 0.5, 0.5)
FREQS = np.arange(1, 50, 2)
POWS = np.arange(0, 2, 0.1)
