"""Settings definitions for methods."""

from apm.sim.settings import FS

###################################################################################################
###################################################################################################

## SPECTRAL FITTING
ALPHA_RANGE = [7, 14]

## IRASA

# Define IRASA settings
IR_F_RANGE = (1, 50)
IRASA_PARAMS = {'fs' : FS, 'f_range' : F_RANGE}

## AUTO-CORRELATION MEASURES

# Settings for autocorrelations
AC_PARAMS = {'max_lag' : 250, 'lag_step' : 1}

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

# Lempel-Ziv complexity
LZ_PARAMS = {'normalize' : False}

## ENTROPY MEASURES

# Sample Entropy
SA_ENT_PARAMS = {'order' : 2}
# Permutation Entropy
PE_ENT_PARAMS = {'order' : 3, 'delay' : 1}
# Approximate Entropy
AP_ENT_PARAMS = {'order' : 2}
# Spectral Entropy
SP_ENT_PARAMS = {'sf' : FS, 'method' : 'fft'}
