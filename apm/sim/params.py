"""Utilities for managing and updating simulation parameters."""

import numpy as np

###################################################################################################
###################################################################################################

# Update aperiodic parameters - exponent
upd_exp = lambda params, val : params.update({'exponent' : val})

# Update aperiodic parameters (in combined signals) - exponent
upd_comb_exp = lambda params, val : params['components']['sim_powerlaw'].update({'exponent' : val})

# Update periodic parameters (in combined signals)
upd_freq = lambda params, val : params['components']['sim_oscillation'].update({'freq' : val})
upd_pow = lambda params, val : params.update({'component_variances' : [1, val]})

UPDATES = {
    'update_exp' : upd_exp,
    'update_comb_exp' : upd_comb_exp,
    'update_freq' : upd_freq,
    'update_pow' : upd_pow,
}


def update_vals(sim_params, values, update):
    """Update simulation parameter values."""

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

    Note: could be added to NDSP?
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
    """Create a generator to sample from a parameter range."""

    # Check that length of values is same as length of probs, if provided
    if np.any(probs):
        if len(values) != len(probs):
            raise ValueError("The number of options must match the number of probabilities.")

    while True:
        yield np.random.choice(values, p=probs)
