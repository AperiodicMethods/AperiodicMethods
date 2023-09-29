"""Code for running simulation experiments."""

import warnings
from copy import deepcopy
from functools import partial
from multiprocessing import Pool, cpu_count

import numpy as np
import pandas as pd
from tqdm.notebook import tqdm

from apm.io import load_pickle
from apm.sim.sim import sig_yielder, sig_yielder_update
from apm.sim.params import UPDATES, update_vals, unpack_param_dict

###################################################################################################
###################################################################################################

def run_sims(sim_func, sim_params, measure_func, measure_params, update, values,
             n_sims=10, avg_func=np.mean, var_func=np.std):
    """Compute a measure of interest across a set of simulations.

    Parameters
    ----------
    sim_func : callable
        A function to create the simulations from.
    sim_params : dict
        Input arguments for `sim_func`.
    measure_func : callable
        A measure function to apply to the simulated data.
    measure_params : dict
        Input arguments for `measure_func`.
    update : {'update_exp', 'update_freq', 'update_pow', 'update_comb_exp'} or callable
        Specifies which parameter to update in simulation parameters.
    values : list or 1d array
        A parameter to step across and re-run measure calculations for.
    n_sims : int, optional, default: 10
        The number of iterations to simulate and calculate measures, per value.
    avg_func : callable, optional, default: np.mean
        The function to calculate the average for a particular parameter value.
    var_func : callable, optional, default: np.std
        The function to calculate the variability for a particular parameter value.

    Returns
    -------
    measures : 1d array
        The results of the measures applied to the set of simulations.

    Notes
    -----
    For each parameter value, the average across `n_sims` simulations is computed and returned.
    """

    update = UPDATES[update] if isinstance(update, str) else update

    avg = [None] * len(values)
    var = [None] * len(values)
    for sp_ind, cur_sim_params in enumerate(update_vals(deepcopy(sim_params), values, update)):

        inst_outs = [None] * n_sims
        for s_ind, sig in enumerate(sig_yielder(sim_func, cur_sim_params, n_sims)):
            inst_outs[s_ind] = measure_func(sig, **measure_params)

        avg[sp_ind] = avg_func(inst_outs, 0)
        var[sp_ind] = var_func(inst_outs, 0)

    return np.array(avg), np.array(var)


def run_sims_load(sims_file, measure_func, measure_params, avg_func=np.mean, var_func=np.std):
    """Run measures across a set of simulations loaded from file."""

    sigs = load_pickle(sims_file, None)
    values = list(sigs.keys())
    n_sims = sigs[values[0]].shape[0]

    avg = [None] * len(values)
    var = [None] * len(values)
    for sp_ind, value in enumerate(values):

        inst_outs = [None] * n_sims
        for s_ind, sig in enumerate(sigs[value]):
            inst_outs[s_ind] = measure_func(sig, **measure_params)

        avg[sp_ind] = avg_func(inst_outs, 0)
        var[sp_ind] = var_func(inst_outs, 0)

    return np.array(avg), np.array(var)


def run_sims_parallel(sim_func, sim_params, measure_func, measure_params, update, values,
                      n_sims=10, avg_func=np.mean, var_func=np.std, n_jobs=-1, pbar=False):
    """Compute a set of measures across simulations, in parallel.

    Notes
    -----
    This function has the same call signature as `run_sims`, with the addition of `n_jobs`.
    """

    n_jobs = cpu_count() if n_jobs == -1 else n_jobs

    # Generator to list
    update = UPDATES[update] if isinstance(update, str) else update
    sim_params = update_vals(deepcopy(sim_params), values, update)
    sim_params = [deepcopy(next(sim_params)) for vi in values]

    # Duplicate sims to equal length of n_sims
    sim_params = [pii for pi in range(len(sim_params)) for pii in [sim_params[pi]] * n_sims]

    with Pool(processes=n_jobs) as pool:

        mapping = pool.imap(partial(_proxy, sim_func=sim_func, measure_func=measure_func,
                                    measure_params=measure_params), sim_params)

        measures = list(tqdm(mapping, desc="Running Simulations",
                             total=len(sim_params), dynamic_ncols=True, disable=not pbar))

    # Reshape array and take mean across n_sims
    measures = np.array(measures)
    remainder = int(measures.size / (len(values) * n_sims))

    if remainder == 1:
        # Cases when measure_func returns a single value
        measures = np.reshape(measures, (len(values), n_sims))
    else:
        # Cases where measure_func returns >1 value
        try:
            measures = np.reshape(measures, (len(values), n_sims, remainder))
        except:
            raise ValueError('The measure function returns an array with varying shape.')

    averages = avg_func(measures, axis=1)
    variability = var_func(measures, axis=1)

    return averages, variability


def _proxy(sim_params, sim_func=None, measure_func=None, measure_params=None):
    """Wrap simulation and measure functions together."""

    return measure_func(sim_func(**sim_params), **measure_params)


def run_comparisons(sim_func, sim_params, measures, samplers, n_sims,
                    return_sim_params=False, verbose=False):
    """Compute multiple measures of interest across the same set of simulations.

    Parameters
    ----------
    sim_func : callable
        A function to create simulated time series.
    sim_params : dict
        Input arguments for `sim_func`.
    measures : dict
        Functions to apply to the simulated data.
        The keys should be functions to apply to the data.
        The values should be a dictionary of parameters to use for the method.
    samplers : dict
        Information for how to sample across parameters for the simulations.
        The keys should be string labels of which parameter to update.
        The values should be data ranges to sample for that parameter.
    n_sims : int
        The number of simulations to run.
    return_sim_params : bool, default: False
        Whether to collect and return the parameters of all the generated simulations.
    verbose : bool, optional, default: False
        Whether to print out simulation parameters.
        Used for checking simulations / debugging.

    Returns
    -------
    results : dict
        Computed results for each measure across the set of simulated data.
    all_sim_params : pd.DataFrame
        Collected simulation parameters across all the simulations.
        Only returned if `return_sim_params` is True.
    """

    results = {func.__name__ : deepcopy(np.zeros(n_sims)) for func in measures.keys()}

    if return_sim_params:
        all_sim_params = []

    for s_ind, (sig, cur_sim_params) in enumerate(\
        sig_yielder_update(sim_func, sim_params, samplers, n_sims, True)):

        if verbose:
            print(cur_sim_params)
        if return_sim_params:
            all_sim_params.append(deepcopy(unpack_param_dict(cur_sim_params)))

        for measure, params in measures.items():
            results[measure.__name__][s_ind] = measure(sig, **params)

    if return_sim_params:
        all_sim_params = pd.DataFrame(all_sim_params)
        # If relevant, set a marker for yes / no if signal has an oscillation
        if 'var_pe' in all_sim_params.columns:
            all_sim_params['has_osc'] = all_sim_params['var_pe'] != 0.
        return results, all_sim_params
    else:
        return results


def run_measures(data, measures, warnings_action='ignore'):
    """Compute multiple measures on empirical recordings.

    Parameters
    ----------
    data : 2d array
        Data to run measures on, organized as [channels, timepoints].
    measures : dict
        Functions to apply to the data.
        The keys should be functions to apply to the data.
        The values should be a dictionary of parameters to use for the method.

    Returns
    -------
    results : dict
        Output measures.
        The keys are labels for each applied method.
        The values are the computed measures for each method.
    """

    # Initialize results
    results = {func.__name__ : np.zeros(data.shape[0]) for func in measures.keys()}

    # Calculate measures on data
    with warnings.catch_warnings():
        warnings.simplefilter(warnings_action)
        for ind, sig in enumerate(data):
            for measure, params in measures.items():
                results[measure.__name__][ind] = measure(sig, **params)

    return results


def run_group_measures(group_data, measures):
    """Compute multiple measures on a group of empirical recordings.

    Parameters
    ----------
    group_data : 3d array
        Data to run measures on, organized as [subjects, channels, timepoints].
    measures : dict
        Functions to apply to the data.
        The keys should be functions to apply to the data.
        The values should be a dictionary of parameters to use for the method.
    """

    n_subjs, n_chs, n_timepoints = group_data.shape
    group_results = {func.__name__ : np.zeros([n_subjs, n_chs]) for func in measures.keys()}

    for sub_ind in range(n_subjs):
        subj_measures = run_measures(np.squeeze(group_data[sub_ind, :, :]), measures)
        for label in subj_measures:
            group_results[label][sub_ind, :] = subj_measures[label]

    return group_results
