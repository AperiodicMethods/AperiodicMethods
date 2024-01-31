"""Set up and definition of measures to apply to empirical datasets."""

# Import custom code
import sys; from pathlib import Path
sys.path.append(str(Path('..').resolve()))
from apm.methods import (autocorr_decay_time, dfa, higuchi_fd, hjorth_complexity, lempelziv,
                         lyapunov, sample_entropy, perm_entropy, specparam, irasa)
from apm.methods.settings import (AC_DECAY_PARAMS, DFA_PARAMS, HFD_PARAMS, HJC_PARAMS,
                                  LZ_PARAMS, LY_PARAMS, SA_ENT_PARAMS, PE_ENT_PARAMS)
from apm.methods.periodic import alpha_power

###################################################################################################
###################################################################################################

###################################################################################################
## TIME SERIES METHODS / SETTINGS

TS_MEASURES = {
    autocorr_decay_time : AC_DECAY_PARAMS,
    dfa : DFA_PARAMS,
    higuchi_fd : HFD_PARAMS,
    hjorth_complexity : HJC_PARAMS,
    lempelziv : LZ_PARAMS,
    sample_entropy : SA_ENT_PARAMS,
    perm_entropy : PE_ENT_PARAMS,
}

###################################################################################################
## General method settings

FS = 500
FS2 = 200
F_RANGE = [3, 40]
F_RANGE_LONG = [1, 75]

###################################################################################################
## FREQUENCY DOMAIN METHODS / SETTINGS - EEG / SHORT

## PSD SETTINGS
PSD_SETTINGS = {
    'f_range' : F_RANGE,
    'fs' : FS,
}

## FREQUENCY DOMAIN METHODS / SETTINGS - EEG / SHORT

PSD_SETTINGS_LONG = {
    'f_range' : F_RANGE_LONG,
    'fs' : FS2,
}

## SPECPARAM SETTINGS

SPECPARAM_SETTINGS = {
    'aperiodic_mode' : 'fixed',
    'min_peak_height' : 0.05,
    'max_n_peaks' : 8,
}

# SPECPARAM_SETTINGS_LONG = {
#     'aperiodic_mode' : 'knee',
#     'min_peak_height' : 0.05,
# }

SPECPARAM_SETTINGS_KNEE = {
    'min_peak_height' : 0.1,
    'peak_width_limits' : [1, 8],
    'max_n_peaks' : 12,
    'aperiodic_mode' : 'knee',
}

## IRASA SETTINGS

IRASA_SETTINGS_LONG = {
    'fit_func' : 'fit_irasa_knee',
}

###################################################################################################

# FREQ_MEASURES = {
#     specparam : PSD_SETTINGS | SPECPARAM_SETTINGS,
#     irasa : PSD_SETTINGS,
# }

# FREQ_MEASURES_LONG = {
#     specparam : PSD_SETTINGS_LONG | SPECPARAM_SETTINGS_LONG,
#     irasa : PSD_SETTINGS_LONG | IRASA_SETTINGS_LONG,
# }

###################################################################################################
## COLLECT MEASURES TOGETHER

# MEASURES = TS_MEASURES | FREQ_MEASURES
# MEASURES_LONG = TS_MEASURES | FREQ_MEASURES_LONG

###################################################################################################
## PEAK MEASURES

# PEAK_MEASURES = {
#     alpha_power : MEASURES[specparam],
# }
