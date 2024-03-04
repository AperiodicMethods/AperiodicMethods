"""Pre-generate some example time series."""

from neurodsp.utils import create_times
from neurodsp.sim import (sim_powerlaw, sim_synaptic_current, sim_knee,
                          sim_oscillation, sim_bursty_oscillation,
                          sim_combined, sim_peak_oscillation)
from neurodsp.utils import set_random_seed

from apm.sim.sim import sim_combined_peak

from apm.sim.defs import SIM_DEFS
from apm.sim.objs import SimParams
from apm.sim.settings import N_SECONDS, FS

###################################################################################################
###################################################################################################

def get_times(n_seconds=N_SECONDS, fs=FS):
    """Helper function to get a times vector for example signals."""

    return create_times(n_seconds, fs)


def get_examples(n_seconds=N_SECONDS, fs=FS):
    """Helper function to get a collection of example signals."""

    set_random_seed(404)

    # Define sim parameters
    sim_params = SimParams(n_seconds, fs)
    sim_params.register_group(SIM_DEFS)

    examples = {

        # Aperiodic time series
        'powerlaw' : sim_powerlaw(**sim_params['ap']),
        'synaptic' : sim_synaptic_current(**sim_params['syn']),
        'knee' : sim_knee(**sim_params['knee']),

        # Oscillatory time series
        'oscillation' : sim_oscillation(**sim_params['osc']),
        'burst' : sim_bursty_oscillation(**sim_params['burst']),

        # Combined time series
        'combined' : sim_combined(**sim_params['comb']),
        'comb-burst' : sim_combined(**sim_params['comb_burst']),
        'comb-peak' : sim_combined_peak(**sim_params['peak']),
    }

    return examples


def check_examples(examples, measure, measure_kwargs, name=None, expected={}):
    """Check application of a given measure to a set of example signals."""

    print('Computed {}:'.format(name if name else 'measure'))
    for label, example in examples.items():
        if label in expected:
            print('  {:15s}: \t {:1.4f} \t{:1.2f}'.format(\
                label, measure(example, **measure_kwargs), expected[label]))
        else:
            print('  {:15s}: \t {:1.4f}'.format(label, measure(example, **measure_kwargs)))
