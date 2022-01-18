"""Default settings file."""

import numpy as np

###################################################################################################
###################################################################################################

# General simulation settings
N_SECONDS = 30
FS = 1000

EXP = -1.5
#F_RANGE = None
F_RANGE = (0.5, None)
FREQ = 10

COMP_VARS = [1, 0.25]

# Collect together simulation parameters
SIM_PARAMS_AP = {'n_seconds' : N_SECONDS, 'fs' : FS, 'f_range' : F_RANGE}
SIM_PARAMS_COMB = {'n_seconds' : N_SECONDS, 'fs' : FS,
                   'components' : {'sim_powerlaw' : {'exponent' : EXP, 'f_range' : F_RANGE},
                                   'sim_oscillation' : {'freq' : FREQ}},
                   'component_variances' : COMP_VARS}
SIM_PARAMS_BURST = {'n_seconds' : N_SECONDS, 'fs' : FS,
                    'components' : {'sim_powerlaw' : {'exponent' : EXP, 'f_range' : F_RANGE},
                                    'sim_bursty_oscillation' : {'freq' : FREQ}},
                    'component_variances' : COMP_VARS}

# Set the number of instances to run
N_SIMS = 50

# Set the range of exponents to explore
EXPS = np.arange(-3, 0.5, 0.5)
FREQS = np.arange(1, 50, 2)
POWERS = np.arange(0, 2, 0.1)
