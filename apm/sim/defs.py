"""Simulation definitions."""

from apm.sim.settings import N_SIMS, N_SIMS2, N_SECONDS, FS
from apm.sim.settings import EXP, EXP1, EXP2, KNEE, F_RANGE, FREQ, BW, HEIGHT, COMP_VARS
from apm.sim.settings import EXPS, TSCALES, KNEES, FREQS, POWERS, CVARS, BWS, BPROBS
from apm.sim.objs import SimParams, SimIters

###################################################################################################
## Define parameters per simulation function

SIM_PARAMS = {

    # Aperiodc Timeseries
    'sim_powerlaw' : {
        'exponent' : EXP,
        'f_range' : F_RANGE,
    },
    'sim_synaptic_current' : {
    },
    'sim_knee' : {
        'exponent1' : EXP1,
        'exponent2' : EXP2,
        'knee' : KNEE,
    },

    # Periodic Timeseries
    'sim_oscillation' : {
        'freq' : FREQ,
    },
    'sim_bursty_oscillation' : {
        'freq' : FREQ,
    },

    # Combined Timeseries
    'sim_peak_oscillation' : {
        'freq' : FREQ,
        'bw' : BW,
        'height' : HEIGHT,
    },
}

###################################################################################################
## Collect group definition of simulations to define

SIM_DEFS = {

    # Aperiodic Signals
    'ap' : SIM_PARAMS['sim_powerlaw'],
    'syn' : SIM_PARAMS['sim_synaptic_current'],
    'knee' : SIM_PARAMS['sim_knee'],

    # Periodic Signals
    'osc' : SIM_PARAMS['sim_oscillation'],
    'burst' : SIM_PARAMS['sim_bursty_oscillation'],

    # Combined Signals
    'comb' : [{
        'sim_powerlaw' : SIM_PARAMS['sim_powerlaw'],
        'sim_oscillation' : SIM_PARAMS['sim_oscillation'],
    },
    {'component_variances' : COMP_VARS},
    ],
    'comb_burst' : [{
        'sim_powerlaw' : SIM_PARAMS['sim_powerlaw'],
        'sim_bursty_oscillation' : SIM_PARAMS['sim_bursty_oscillation'],
    },
    {'component_variances' : COMP_VARS},
    ],
    'peak' : [{
        'sim_powerlaw' : SIM_PARAMS['sim_powerlaw'],
        'sim_peak_oscillation' : SIM_PARAMS['sim_peak_oscillation'],
    }],
}

###################################################################################################
## Collect group definition of simulation parameter iterators

ITER_DEFS = [

    ['ap_exp', 'ap', 'exponent', EXPS],
    ['comb_exp', 'comb', 'exponent', EXPS, 'sim_powerlaw'],
    ['syn_tscales', 'syn', 'tau_d', TSCALES],
    ['kn_knee', 'knee', 'knee', KNEES],

    ['osc_freq', 'comb', 'freq', FREQS, 'sim_oscillation'],
    #['osc_pow', 'comb', 'component_variances', POWERS],
    ['osc_pow', 'comb', 'component_variances', CVARS],

    ['peak_freq', 'peak', 'freq', FREQS, 'sim_peak_oscillation'],
    ['peak_pow', 'peak', 'height', POWERS, 'sim_peak_oscillation'],
    ['peak_bw', 'peak', 'bw', BWS, 'sim_peak_oscillation'],

    ['comb_burst', 'comb_burst', 'enter_burst', BPROBS, 'sim_bursty_oscillation'],
]

###################################################################################################
## Define simulation parameter and simulation iterator objects

# ...
SIM_PARAMS = SimParams(N_SECONDS, FS)
SIM_PARAMS.register_group(SIM_DEFS)

# ...
SIM_ITERS = SimIters(N_SECONDS, FS)
SIM_ITERS.register_group(SIM_DEFS)
SIM_ITERS.register_group_iters(ITER_DEFS)
