"""Define settings for simulations."""

import pkg_resources

import numpy as np

###################################################################################################
###################################################################################################

N_PEAK_OPTS = [0, 1, 2]
N_PEAK_PROBS = [1/3, 1/3, 1/3]

CF_OPTS = np.load(pkg_resources.resource_filename(__name__, 'data/freqs.npy'))
CF_PROBS = np.load(pkg_resources.resource_filename(__name__, 'data/probs.npy'))

PW_OPTS = [0.05, 0.10, 0.15, 0.20]
PW_PROBS = [0.25, 0.25, 0.25, 0.25]

BW_OPTS = [1, 1.5, 2]
BW_PROBS = [1/3, 1/3, 1/3]
