"""Utilities for managing and updating simulation parameters."""

import numpy as np

###################################################################################################
## Define update functions

# Update aperiodic parameters - exponent
upd_exp = lambda params, val : \
    params.update({'exponent' : val})

# Update aperiodic parameters (in combined signals) - exponent
upd_comb_exp = lambda params, val : \
    params['components']['sim_powerlaw'].update({'exponent' : val})

# Update aperiodic parameters - knee
upd_knee = lambda params, val : \
    params.update({'tau_d' : val})

# Update periodic parameters (in combined signals)
upd_freq = lambda params, val : \
    params['components']['sim_oscillation'].update({'freq' : val})
upd_pow = lambda params, val : \
    params.update({'component_variances' : [1, val]})

# Update periodic parameters (in combined peak signals)
upd_peak_freq = lambda params, val : \
    params['components']['sim_peak_oscillation'].update({'freq' : val})
upd_peak_hgt = lambda params, val : \
    params['components']['sim_peak_oscillation'].update({'height' : val})
upd_peak_bw = lambda params, val : \
    params['components']['sim_peak_oscillation'].update({'bw' : val})

###################################################################################################
## Collect together all update function

UPDATES = {
    'update_exp' : upd_exp,
    'update_comb_exp' : upd_comb_exp,
    'update_knee' : upd_knee,
    'update_freq' : upd_freq,
    'update_pow' : upd_pow,
    'update_peak_freq' : upd_peak_freq,
    'update_peak_hgt' : upd_peak_hgt,
    'update_peak_bw' : upd_peak_bw,
}

###################################################################################################
## Functions for updating / sampling paramters

def update_sim_params(sim_params, samplers):
    """Update a simulation parameter definition from set of samplers.

    Parameters
    ----------
    sim_params : dict
        The parameters for the simulated signal.
    samplers : dict
        Dictionary of samplers to update simulation parameters.

    Returns
    -------
    sim_params : dict
        The updated parameters for the simulated signal.
    """

    for key, val in samplers.items():
        UPDATES[key](sim_params, next(val))

    return sim_params


def update_vals(sim_params, values, update):
    """Update simulation parameter values.

    Parameters
    ----------
    sim_params : dict
        The parameters for the simulated signal.
    values : list or 1d array
        Parameter values to update across.
    update : callable
        Function to use to apply update to `sim_params`.

    Yields
    ------
    sim_params : dict
        The parameters for the simulated signal.
    """

    for val in values:
        update(sim_params, val)
        yield sim_params


def unpack_param_dict(params):
    """Unpack a dictionary of simulation parameters into a flattened dictionary.

    Parameters
    ----------
    params : dict
        Dictionary of simulation parameters.

    Returns
    -------
    nparams : dict
        Flattened dictionary of simulation parameters.

    ToDo / Note: could be added to NDSP?
    """

    nparams = {}
    for key, value in params.items():
        if key == 'components':
            for key2 in params['components']:
                nparams.update(params['components'][key2])
        elif key == 'component_variances':
            for var_label, var_val in zip(['var_ap', 'var_pe'], params['component_variances']):
                nparams[var_label] = var_val
        else:
            nparams[key] = value

    return nparams


def sampler(values, probs=None):
    """Create a generator to sample from a parameter range.

    Parameters
    ----------
    values : list or 1d array
        Parameter values to create a generator for.
    probs : 1d array, optional
        Probabilities to sample from values.
        If provided, should be the same lengths as `values`.

    Yields
    ------
    generator
        Generator to sample parameter values from.
    """

    # Check that length of values is same as length of probs, if provided
    if np.any(probs):
        if len(values) != len(probs):
            raise ValueError("The number of options must match the number of probabilities.")

    while True:
        yield np.random.choice(values, p=probs)
