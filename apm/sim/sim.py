"""Additional simulation functions & helpers."""

from copy import deepcopy

import numpy as np

from apm.sim.params import update_sim_params
from apm.sim.utils import counter

###################################################################################################
###################################################################################################

def sig_yielder(sim_func, sim_params, n_sims):
    """Generator to yield simulated signals from a given simulation function and parameters.

    Parameters
    ----------
    sim_func : callable
        Function to create the simulated time series.
    sim_params : dict
        The parameters for the simulated signal, passed into `sim_func`.
    n_sims : int, optional
        Number of simulations to set as the max.
        If None, creates an infinite generator.

    Yields
    ------
    sig : 1d array
        Simulated time series.
    """

    for _ in counter(n_sims):
        yield sim_func(**sim_params)


def sig_sampler(sim_func, sim_params, return_sim_params=False, n_sims=None):
    """Generator to yield simulated signals from a parameter sampler.

    Parameters
    ----------
    sim_func : callable
        Function to create the simulated time series.
    sim_params : iterable
        The parameters for the simulated signal, passed into `sim_func`.
    return_sim_params : bool, optional, default: False
        Whether to yield the simulation parameters as well as the simulated time series.
    n_sims : int, optional
        Number of simulations to set as the max.
        If None, creates an infinite generator.

    Yields
    ------
    sig : 1d array
        Simulated time series.
    sample_params : dict
        Simulation parameters for the yielded time series.
    """

    if len(sim_params) and n_sims and n_sims > len(sim_params):
        msg = 'Cannot simulate the requested number of sims with the given parameters.'
        raise ValueError(msg)

    for ind, sample_params in zip(counter(n_sims), sim_params):

        if return_sim_params:
            yield sim_func(**sample_params), sample_params
        else:
            yield sim_func(**sample_params)

        if n_sims and ind >= n_sims:
            break

# # TO UPDATE / REFACTOR OUT
# def sig_yielder_update(sim_func, sim_params, samplers, n_sims, return_sim_params=False):
#     """Generator to yield simulated signals from a given simulation function and parameters.

#     Parameters
#     ----------
#     sim_func : callable
#         Function to create the simulated time series.
#     sim_params : dict
#         The parameters for the simulated signal, passed into `sim_func`.
#     samplers : dict
#         Dictionary of samplers to update simulation parameters.
#     n_sims : int
#         Number of simulations to set as the max.
#     return_sim_params : bool, optional, default: False
#         Whether to also yield the simulation parameters for each simulated signal.

#     Yields
#     ------
#     sig : 1d array
#         Simulated time series.
#     sim_params : dict
#         Simulation parameters for the current simulated signal.
#         Only returned if `return_sim_params` is True.
#     """

#     # Take a copy of simulation parameters and initialize first update
#     cur_sim_params = update_sim_params(deepcopy(sim_params), samplers)

#     for _ in range(n_sims):

#         cur_sim_params = update_sim_params(cur_sim_params, samplers)
#         cur_sig = sim_func(**cur_sim_params)

#         if return_sim_params:
#             yield cur_sig, cur_sim_params
#         else:
#             yield cur_sig


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


def sim_across_values(sim_func, sim_params, n_sims, output='dict'):
    """Helper function to create a set of simulations across different parameter values.

    Parameters
    ----------
    sim_func : callable
        Function to create the simulated time series.
    sim_params : iterable or list of dict
        Simulation parameters for `sim_func`.
    n_sims : int
        Number of simulations to create per parameter definition.
    output : {'dict', 'array'}
        Organization of the output for the sims.
        If 'dict', stored in a dictionary, organized by simulation parameter.
        If 'array', all sims are organized into a 2D array.

    Returns
    -------
    sims : dict of {float : array} or array
        If dict, dictionary of simulated signals, where:
            Each key is the simulation parameter value for the set of simulations.
            Each value is the set of simulations for that value, as [n_sims, sig_length].
        If array, is all signals collected together as [n_sims, sig_length].
    """

    sims = {}
    for ind, cur_sim_params in enumerate(sim_params):
        label = sim_params.values[ind] if hasattr(sim_params, 'values') else ind
        label = label[-1] if isinstance(label, list) else label
        sims[label] = sim_multiple(sim_func, cur_sim_params, n_sims)
    if output == 'array':
        sims = np.squeeze(np.array(list(sims.values())))

    return sims
