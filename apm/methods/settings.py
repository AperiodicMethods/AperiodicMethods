"""Settings definitions for methods."""

from apm.sim.settings import FS

###################################################################################################
###################################################################################################

## SPECTRAL FITTING

# Frequency range
FIT_F_RANGE = (1, 50)
FIT_F_RANGE_LONG = (1, 100)
ALPHA_RANGE = [7, 14]

# SpecParam settings
SPECPARAM_PARAMS = {
    'fs' : FS,
    'f_range' : FIT_F_RANGE,
    'min_peak_height' : 0.05,
}

SPECPARAM_PARAMS_KNEE = {
    'fs' : FS,
    'f_range' : FIT_F_RANGE_LONG,
    'min_peak_height' : 0.05,
    'aperiodic_mode' : 'knee',
}

# IRASA settings
IRASA_PARAMS = {
    'fs' : FS,
    'f_range' : FIT_F_RANGE,
}
IRASA_PARAMS_KNEE = {
    'fs' : FS,
    'f_range' : FIT_F_RANGE_LONG,
    'fit_func' : 'fit_irasa_knee',
}

## AUTO-CORRELATION MEASURES

# Settings for autocorrelations
AC_PARAMS = {
    'max_lag' : 250,
    'lag_step' : 1,
}
AC_DECAY_PARAMS = {
    'fs' : FS,
    'max_lag' : 1500,
    'lag_step' : 2,
    'level' : 0.5,
}
#DECAY_LEVEL = 0.5

## FLUCTUATION METHODS

# Hurst settings
HURST_PARAMS = {
    'fs' : FS,
    'n_scales' : 10,
    'min_scale' : 0.1,
    'max_scale' : 2.0
}

# DFA settings
DFA_PARAMS = {
    'fs' : FS,
    'n_scales' : 10,
    'min_scale' : 0.1,
    'max_scale' : 2.0,
    'deg' : 1
}

## COMPLEXITY MEASURES

# Hjorth measures
HJM_PARAMS = {}
HJC_PARAMS = {}

# Lempel-Ziv complexity
LZ_PARAMS = {
    'normalize' : False,
}

# Lyapunov exponent
LY_PARAMS = {}

## FRACTAL MEASURES

HFD_PARAMS = {}
KFD_PARAMS = {}
PFD_PARAMS = {}
SFD_PARAMS = {}

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
    'sf' : FS,
    'method' : 'fft',
}

## MULTISCALE ENTROPY MEASURES

# Multiscale Approximate Entropy
MULTI_AP_ENT_PARAMS = {}
# Multiscale Sample Entropy
MULTI_SA_ENT_PARAMS = {}
# Multiscale Permutation Entropy
MULTI_PE_ENT_PARAMS = {}
# Multiscale Weighted Permutation Entropy
MULTI_WPE_ENT_PARAMS = {}
