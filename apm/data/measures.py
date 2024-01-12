"""   """

# Import custom code
import sys; from pathlib import Path
sys.path.append(str(Path('..').resolve()))
from apm.methods import (autocorr_decay_time, dfa, higuchi_fd, lempelziv, lyapunov,
                         sample_entropy, perm_entropy, specparam, irasa)
from apm.methods.settings import (AC_DECAY_PARAMS, DFA_PARAMS, HFD_PARAMS, LZ_PARAMS,
                                  LY_PARAMS, SA_ENT_PARAMS, PE_ENT_PARAMS)
from apm.methods.periodic import alpha_power

###################################################################################################
###################################################################################################

# General method settings
F_RANGE = [3, 40]
FS = 500

PSD_SETTINGS = {
    'f_range' : F_RANGE,
    'fs' : FS
}

#
SPECPARAM_SETTINGS = {
    'min_peak_height' : 0.05,
}

# Define measures to apply
MEASURES = {
    autocorr_decay_time : AC_DECAY_PARAMS,
    #hurst : HURST_PARAMS,
    dfa : DFA_PARAMS,
    #higuchi_fd : HFD_PARAMS,
    #hjorth_complexity : HJC_PARAMS,
    lempelziv : LZ_PARAMS,
    sample_entropy : SA_ENT_PARAMS,
    perm_entropy : PE_ENT_PARAMS,
    specparam : PSD_SETTINGS | SPECPARAM_SETTINGS,
    irasa : PSD_SETTINGS,
}

## PEAK MEASURES

PEAK_MEASURES = {
    alpha_power : MEASURES[specparam],
}
