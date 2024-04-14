"""Simulation definitions."""

from copy import deepcopy

import numpy as np

from neurodsp.sim.update import create_updater, create_sampler
from neurodsp.sim.params import SimParams, SimIters, SimSamplers

from apm.sim.settings import N_SAMPLES, N_SECONDS, FS
from apm.sim.settings import EXP, EXP1, EXP2, KNEE, F_RANGE, FREQ, BW, HEIGHT, COMP_VARS
from apm.sim.settings import EXPS, TSCALES, KNEES, FREQS, POWERS, CVARS, BWS, BPROBS

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
        'component' : 'sim_peak_oscillation',
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
## Collect group definition of simulation parameter samplers

SAMPLER_VALS = {
    'exp' : np.round(np.arange(-2.5, 0.1, 0.1), 1)
}

SAMPLER_DEFS = [

    {
        'name' : 'exp_sampler',
        'label' : 'ap',
        'samplers' : {
            create_updater('exponent') : create_sampler(deepcopy(SAMPLER_VALS['exp'])),
        },
    },

    {
        'name' : 'tscale_sampler',
        'label' : 'syn',
        'samplers' : {
            create_updater('tau_d') : \
                create_sampler(np.round(np.array([0.005, 0.015, 0.030, 0.050, 0.075]), 3)),
        },
    },

    {
        'name' : 'knee_sampler',
        'label' : 'knee',
        'samplers' : {
            create_updater('knee') : \
                create_sampler([10, 25, 100, 200, 400, 700, 900, 1200, 1600, 2500]),
            create_updater('exponent2') : \
                create_sampler(np.round(np.arange(-2.5, -1.0, 0.25), 1)),
        },
    },

    {
        'name' : 'comb_sampler',
        'label' : 'comb',
        'samplers' : {
            create_updater('exponent', 'sim_powerlaw') : \
                create_sampler(deepcopy(SAMPLER_VALS['exp'])),
            create_updater('component_variances') : \
                create_sampler([[1, val] for val in np.round(np.arange(0, 1.1, 0.1), 1)],
                               probs = [0.30] + ([0.07] * 10)),
            create_updater('freq', 'sim_oscillation') : create_sampler(np.arange(5, 36, 1)),
        },
    },

    {
        'name' : 'peak_sampler',
        'label' : 'peak',
        'samplers' : {
            create_updater('exponent', 'sim_powerlaw') : \
                create_sampler(deepcopy(SAMPLER_VALS['exp'])),
            create_updater('freq', 'sim_peak_oscillation') : \
                create_sampler(np.arange(8, 30, 1)),
            create_updater('height', 'sim_peak_oscillation') : \
                create_sampler(np.round(np.arange(1.0, 2.25, 0.25), 2)),
            create_updater('bw', 'sim_peak_oscillation') : \
                create_sampler(np.round(np.arange(1.0, 5.5, 0.5), 1)),
        },
    },

]

###################################################################################################
## Define simulation parameter and simulation iterator objects

# Collect and define simulation parameters
SIM_PARAMS = SimParams(N_SECONDS, FS)
SIM_PARAMS.register_group(SIM_DEFS)

# Collect and define simulation iterators
SIM_ITERS = SimIters(N_SECONDS, FS)
SIM_ITERS.register_group(SIM_DEFS)
SIM_ITERS.register_group_iters(ITER_DEFS)

# Collect and define simulation samplers
SIM_SAMPLERS = SimSamplers(N_SECONDS, FS, N_SAMPLES)
SIM_SAMPLERS.register_group(SIM_DEFS)
SIM_SAMPLERS.register_group_samplers(SAMPLER_DEFS)
