"""Settings definitions for methods."""

from copy import deepcopy

from apm.sim.settings import FS

###################################################################################################
###################################################################################################

## AUTO-CORRELATION MEASURES

# Settings for autocorrelations
AC_PARAMS = {
    'max_lag' : 250,
    'lag_step' : 1,
}

AC_DECAY_PARAMS = {
    'fs' : None,
    'max_lag' : 1500,
    'lag_step' : 2,
    'level' : 0.5,
}

## FLUCTUATION METHODS

# Hurst settings
HURST_PARAMS = {
    'fs' : None,
    'n_scales' : 10,
    'min_scale' : 0.1,
    'max_scale' : 2.0
}

# DFA settings
DFA_PARAMS = {
    'fs' : None,
    'n_scales' : 10,
    'min_scale' : 0.1,
    'max_scale' : 2.0,
    'deg' : 1,
}

## FRACTAL MEASURES

# Correlation dimension
CD_PARAMS = {
    'delay' : 4,
    'dimension' : 20,
}

# Fractal dimension
HFD_PARAMS = {}
KFD_PARAMS = {}
PFD_PARAMS = {}
SFD_PARAMS = {}

## COMPLEXITY MEASURES

# Hjorth measures
HJA_PARAMS = {}
HJM_PARAMS = {}
HJC_PARAMS = {}

# Lempel-Ziv complexity
LZ_PARAMS = {
    'normalize' : False,
}

# Lyapunov exponent
LY_PARAMS = {
    'delay' : 4,
    'dimension' : 20,
}

## ENTROPY MEASURES

# Approximate Entropy
AP_ENT_PARAMS = {
    'order' : 2,
}

# Sample Entropy
SA_ENT_PARAMS = {
    'order' : 2,
}

# Permutation Entropy
PE_ENT_PARAMS = {
    'order' : 3,
    'delay' : 1,
}

# Weighted Permutation Entropy
WPE_ENT_PARAMS = {
    'order' : 3,
    'delay' : 1,
}

# Spectral Entropy
SP_ENT_PARAMS = {
    'sf' : None,
    'method' : 'fft',
}

## MULTISCALE ENTROPY MEASURES

# Multiscale Approximate Entropy
MAP_ENT_PARAMS = {}

# Multiscale Sample Entropy
MSA_ENT_PARAMS = {}

# Multiscale Permutation Entropy
MPE_ENT_PARAMS = {}

# Multiscale Weighted Permutation Entropy
MWPE_ENT_PARAMS = {}

## SPECTRAL FITTING

# Frequency range
FIT_F_RANGE = (1, 50)
FIT_F_RANGE_LONG = (1, 100)
ALPHA_RANGE = (7, 14)

# Spectral fit settings
SPECTRAL_FIT_SETTINGS = {
    'fs' : None,
    'f_range' : FIT_F_RANGE,
}

SPECTRAL_FIT_SETTINGS_LONG = {
    'fs' : None,
    'f_range' : FIT_F_RANGE_LONG,
}

# SpecParam settings
SPECPARAM_SETTINGS = {
    'max_n_peaks' : 8,
    'peak_width_limits' : [1, 8],
    'min_peak_height' : 0.05,
    'aperiodic_mode' : 'fixed',
}

SPECPARAM_PARAMS = deepcopy(SPECTRAL_FIT_SETTINGS) | deepcopy(SPECPARAM_SETTINGS)

SPECPARAM_SETTINGS_KNEE = {
    'max_n_peaks' : 12,
    'peak_width_limits' : [1, 8],
    'min_peak_height' : 0.1,
    'aperiodic_mode' : 'knee',
}

SPECPARAM_PARAMS_KNEE = deepcopy(SPECTRAL_FIT_SETTINGS_LONG) | deepcopy(SPECPARAM_SETTINGS_KNEE)

# IRASA settings
IRASA_SETTINGS = {}

IRASA_PARAMS = deepcopy(SPECTRAL_FIT_SETTINGS) | deepcopy(IRASA_SETTINGS)

IRASA_SETTINGS_KNEE = {
    'fit_func' : 'fit_irasa_knee',
}

IRASA_PARAMS_KNEE = deepcopy(SPECTRAL_FIT_SETTINGS) | deepcopy(IRASA_SETTINGS_KNEE)
