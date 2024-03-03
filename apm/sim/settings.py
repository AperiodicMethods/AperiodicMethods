"""Simulation settings."""

from copy import deepcopy

import numpy as np

###################################################################################################
## Define general simulation settings

# Set the number of instances to run
N_SIMS = 50
N_SIMS2 = 10

# General simulation settings
N_SECONDS = 30
FS = 250
FS2 = 500

###################################################################################################
## Define default parameter values

# Define aperiodic parameters
EXP = -1.5
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
COMP_VARS = [1, 0.25]

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

###################################################################################################
## Define parameters per component

# AP_PARAMS = {
#     'sim_powerlaw' : {
#         'exponent' : EXP,
#         'f_range' : F_RANGE,
#     }
# }

# KNEE_PARAMS = {
#     'sim_knee' : {
#         'exponent1' : 0,
#         'exponent2' : -2,
#         'knee' : 0,
#     }
# }

# OSC_PARAMS = {
#     'sim_oscillation' : {
#         'freq' : FREQ,
#     }
# }

# PEAK_PARAMS = {
#     'sim_peak_oscillation' : {
#         'freq' : FREQ,
#         'bw' : BW,
#         'height' : HEIGHT,
#     }
# }

# BURST_PARAMS = {
#     'sim_bursty_oscillation' : {
#         'freq' : FREQ,
#     }
# }

###################################################################################################
## Define collected simulation parameters for different simulation functions

# # Define base set of simulation parameters
# BASE_PARAMS = {
#     'n_seconds' : N_SECONDS,
#     'fs' : FS,
# }

# # Sim parameters for powerlaw aperiodic signal
# SIM_PARAMS_AP = deepcopy(BASE_PARAMS)
# SIM_PARAMS_AP.update({
#     'f_range' : F_RANGE,
# })

# # Sim parameters for synaptic current / knee signal
# SIM_PARAMS_KNEE = deepcopy(BASE_PARAMS)

# # TEMP
# SIM_PARAMS_KNEE2 = deepcopy(BASE_PARAMS)
# SIM_PARAMS_KNEE2.update({
#     'exponent1' : 0,
#     'exponent2' : -2,
#     'knee' : 0,
# })

# # Sim parameters for combined aperiodic & periodic signal
# SIM_PARAMS_COMB = deepcopy(BASE_PARAMS)
# SIM_PARAMS_COMB.update({
#     'components' : {
#         **deepcopy(AP_PARAMS),
#         **deepcopy(OSC_PARAMS),
#     },
#     'component_variances' : COMP_VARS,
# })

# # Sim parameters for combined signal with a wide peak
# SIM_PARAMS_PEAK = deepcopy(BASE_PARAMS)
# SIM_PARAMS_PEAK.update({
#     'components' : {
#         **deepcopy(AP_PARAMS),
#         **deepcopy(PEAK_PARAMS),
#     }
# })

# # Sim parameters for combined signal with a bursty oscillation
# SIM_PARAMS_BURST = deepcopy(BASE_PARAMS)
# SIM_PARAMS_BURST.update({
#     'components' : {
#         **deepcopy(AP_PARAMS),
#         **deepcopy(BURST_PARAMS),
#     },
#     'component_variances' : COMP_VARS,
# })
