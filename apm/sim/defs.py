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

    # Aperiodic Parameter Iterators
    {
        'name' : 'ap_exp',
        'label' : 'ap',
        'update' : 'exponent',
        'values' : EXPS,
    },
    {
        'name' : 'comb_exp',
        'label' : 'comb',
        'update' : 'exponent',
        'values' : EXPS,
        'component' : 'sim_powerlaw'
    },
    {
        'name' : 'syn_tscales',
        'label' : 'syn',
        'update' : 'tau_d',
        'values' : TSCALES,
    },
    {
        'name' : 'kn_knee',
        'label' : 'knee',
        'update' : 'knee',
        'values' : KNEES,
    },

    # Periodic Parameter Iterators
    {
        'name' : 'osc_freq',
        'label' : 'comb',
        'update' : 'freq',
        'values' : FREQS,
        'component' : 'sim_oscillation',
    },
    {
        'name' : 'osc_pow',
        'label' : 'comb',
        'update' : 'component_variances',
        'values' : CVARS,
    },

    # Peak Simulation Iterators
    {
        'name' : 'peak_freq',
        'label' : 'peak',
        'update' : 'freq',
        'values' : FREQS,
        'component' : 'sim_peak_oscillation',
    },
    {
        'name' : 'peak_pow',
        'label' : 'peak',
        'update' : 'height',
        'values' : POWERS,
        'component' : 'sim_peak_oscillation',
    },
    {
        'name' : 'peak_bw',
        'label' : 'peak',
        'update' : 'bw',
        'values' : BWS,
        'component' : ' sim_peak_oscillation',
    },

    # Bursty Oscillation Iterators
    {
        'name' : 'comb_burst',
        'label' : 'comb_burst',
        'update' : 'enter_burst',
        'values' : BPROBS,
        'component' : 'sim_bursty_oscillation',
    },
]

###################################################################################################
## Define simulation parameter and simulation iterator objects

# Collect and define simulation parameters
SIM_PARAMS = SimParams(N_SECONDS, FS)
SIM_PARAMS.register_group(SIM_DEFS)

# Collect and defined simulation iterators
SIM_ITERS = SimIters(N_SECONDS, FS)
SIM_ITERS.register_group(SIM_DEFS)
SIM_ITERS.register_group_iters(ITER_DEFS)
