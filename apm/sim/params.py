"""Utilities for managing and updating simulation parameters."""

import numpy as np

from apm.sim.utils import counter

###################################################################################################
## Functions for updating / sampling paramters

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


def create_sampler(values, probs=None, n_samples=None):
    """Create a generator to sample from a parameter range.

    Parameters
    ----------
    values : list or 1d array
        Parameter values to create a generator for.
    probs : 1d array, optional
        Probabilities to sample from values.
        If provided, should be the same lengths as `values`.
    n_samples : int, optional
        The number of parameter iterations to set as max.
        If None, creates an infinite generator.

    Yields
    ------
    generator
        Generator to sample parameter values from.
    """

    # Check that length of values is same as length of probs, if provided
    if np.any(probs):
        if len(values) != len(probs):
            raise ValueError("The number of options must match the number of probabilities.")

    for _ in counter(n_samples):

        if isinstance(values[0], (list, np.ndarray)):
            yield values[np.random.choice(len(values), p=probs)]
        else:
            yield np.random.choice(values, p=probs)
