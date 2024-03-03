"""Additional simulation functions & helpers."""

from copy import deepcopy

import numpy as np

from neurodsp.sim.info import get_sim_func
from neurodsp.sim.combined import sim_peak_oscillation

#from apm.sim.params import update_sim_params

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


def sig_yielder_update(sim_func, sim_params, samplers, n_sims, return_sim_params=False):
    """Generator to yield a simulated signals from a given simulation function and parameters.

    Parameters
    ----------
    sim_func : callable
        Function to create the simulated time series.
    sim_params : dict
        The parameters for the simulated signal, passed into `sim_func`.
    samplers : dict
        Dictionary of samplers to update simulation parameters.
    n_sims : int
        Number of simulations to set as the max.
    return_sim_params : bool, optional, default: False
        Whether to also yield the simulation parameters for each simulated signal.

    Yields
    ------
    sig : 1d array
        Simulated time series.
    sim_params : dict
        Simulation parameters for the current simulated signal.
        Only returned if `return_sim_params` is True.
    """

    # Take a copy of simulation parameters and initialize first update
    cur_sim_params = update_sim_params(deepcopy(sim_params), samplers)

    for _ in range(n_sims):

        cur_sim_params = update_sim_params(cur_sim_params, samplers)
        cur_sig = sim_func(**cur_sim_params)

        if return_sim_params:
            yield cur_sig, cur_sim_params
        else:
            yield cur_sig


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


def sim_across_values(sim_func, sim_params, n_sims):
    """Helper function to create a set of simulations across different parameter values.

    Parameters
    ----------
    sim_func : callable
        Function to create the simulated time series.
    sim_params : iterable or list of dict
        Simulation parameters for `sim_func`.
    n_sims : int
        Number of simulations to create.

    Returns
    -------
    sims : dict of {float : array}
        Dictionary of simulated signals.
        Each key is the simulation parameter value for the set of simulations.
        Each value is the set of simulations for that value, as [n_sims, sig_length].
    """

    sims = {}
    for ind, cur_sim_params in enumerate(sim_params):
        label = sim_params.values[ind] if hasattr(sim_params, 'values') else ind
        label = label[-1] if isinstance(label, list) else label
        sims[label] = sim_multiple(sim_func, cur_sim_params, n_sims)

    return sims


def sim_combined_peak(n_seconds, fs, components):
    """Simulate a combined signal with an aperiodic component and a peak.

    Parameters
    ----------
    n_seconds : float
        Simulation time, in seconds.
    fs : float
        Sampling rate of simulated signal, in Hz.
    components : dict
        A dictionary of simulation functions to run, with their desired parameters.

    Returns
    -------
    sig : 1d array
        Simulated combined peak signal.
    """

    sim_names = list(components.keys())
    assert len(sim_names) == 2, 'Expected only 2 components.'
    assert sim_names[1] == 'sim_peak_oscillation', \
        'Expected `sim_peak_oscillation` as the second key.'

    ap_func = get_sim_func(sim_names[0]) if isinstance(sim_names[0], str) else sim_names[0]

    sig = sim_peak_oscillation(\
        ap_func(n_seconds, fs, **components[sim_names[0]]), fs, **components[sim_names[1]])

    return sig


# Alternative implementation of the above - probably to drop:
# def sim_combined_peak(n_seconds, fs, ap_func, ap_params, peak_params):

#     sig_ap = ap_func(n_seconds, fs, **ap_params)
#     sig = sim_peak_oscillation(sig_ap, fs, **peak_params)

#     return sig
