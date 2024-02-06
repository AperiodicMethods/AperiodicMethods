"""Settings for the analysis scripts."""

# Import custom code
import sys; from pathlib import Path
sys.path.append(str(Path('..').resolve()))
from apm.methods import (autocorr_decay_time, dfa, higuchi_fd, hjorth_complexity, lempelziv,
                         sample_entropy, perm_entropy, specparam, irasa)
from apm.methods.settings import (AC_DECAY_PARAMS, DFA_PARAMS, HFD_PARAMS, HJC_PARAMS,
                                  LZ_PARAMS, SA_ENT_PARAMS, PE_ENT_PARAMS)

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

## SPECPARAM SETTINGS

SPECPARAM_SETTINGS = {
    'max_n_peaks' : 8,
    'peak_width_limits' : [1, 8],
    'min_peak_height' : 0.05,
    'aperiodic_mode' : 'fixed',
}

SPECPARAM_SETTINGS_KNEE = {
    'max_n_peaks' : 12,
    'peak_width_limits' : [1, 8],
    'min_peak_height' : 0.1,
    'aperiodic_mode' : 'knee',
}
