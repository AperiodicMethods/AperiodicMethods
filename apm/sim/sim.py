"""Additional simulation functions & helpers."""

from copy import deepcopy

import numpy as np

from neurodsp.sim.info import get_sim_func
from neurodsp.sim.combined import sim_peak_oscillation

from apm.sim.params import UPDATES, update_vals

###################################################################################################
###################################################################################################

def sig_yielder(sim_func, sim_params, n_sims):
    """Generator to yield a simulated signals from a given simulation function and parameters.

    Parameters
    ----------
    sim_func : callable
        Function to create the simulated time series.
    sim_params : dict
        The parameters for the simulated signal, passed into `sim_func`.
    n_sims : int
        Number of simulations to set as the max.

    Yields
    ------
    sig : 1d array
        Simulated time series.
    """

    for _ in range(n_sims):
        yield sim_func(**sim_params)


def sim_multiple(sim_func, sim_params, n_sims):
    """Simulate multiple samples of a specified simulation.

    Parameters
    ----------
    sim_func : callable
        Function to create the simulated time series.
    sim_params : dict
        The parameters for the simulated signal, passed into `sim_func`.
    n_sims : int
        Number of simulations to create.

    Returns
    -------
    sigs : 2d array
        Simulations, as [n_sims, sig length].
    """

    sigs = np.zeros([n_sims, sim_params['n_seconds'] * sim_params['fs']])
    for ind, sig in enumerate(sig_yielder(sim_func, sim_params, n_sims)):
        sigs[ind, :] = sig

    return sigs


def sim_across_values(sim_func, sim_params, update, values, n_sims):
    """Helper function to create a set of simulations across different parameter values."""

    update = UPDATES[update] if isinstance(update, str) else update

    sims = {}
    for val, cur_sim_params in zip(values, update_vals(deepcopy(sim_params), values, update)):
        sims[val] = sim_multiple(sim_func, cur_sim_params, n_sims)

    return sims


def sim_combined_peak(n_seconds, fs, components):
    """Simulate a combined signal with an aperiodic component and a peak."""

    sim_names = list(components.keys())
    assert len(sim_names) == 2, 'Expected only 2 components.'
    assert sim_names[1] == 'sim_peak_oscillation', \
        'Expected `sim_peak_oscillation` as the second key.'

    ap_func = get_sim_func(sim_names[0]) if isinstance(sim_names[0], str) else sim_names[0]

    sig = sim_peak_oscillation(\
        ap_func(n_seconds, fs, **components[sim_names[0]]), fs, **components[sim_names[1]])

    return sig

# Alternative implementation - probably to drop:
# def sim_combined_peak(n_seconds, fs, ap_func, ap_params, peak_params):

#     sig_ap = ap_func(n_seconds, fs, **ap_params)
#     sig = sim_peak_oscillation(sig_ap, fs, **peak_params)

#     return sig
