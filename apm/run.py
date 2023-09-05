"""Code for running simulation experiments."""

from copy import deepcopy

from multiprocessing import Pool, cpu_count
from functools import partial
from tqdm.notebook import tqdm

import numpy as np
import pandas as pd

from bootstrap import bootstrap_corr

from apm.utils import unpack_param_dict

###################################################################################################
###################################################################################################

# Update aperiodic parameters
upd_exp = lambda params, val : params.update({'exponent' : val})

# Update aperiodic parameters (in combined signals)
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


def run_sims(sim_func, sim_params, measure_func, measure_params, update, values,
             n_sims=10, avg_func=np.mean, var_func=None):
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
    var_func : callable, optional
        The function to calculate the variability for a particular parameter value.
        If None, variability is not computed.

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
    var = np.zeros(len(values))
    for sp_ind, cur_sim_params in enumerate(update_vals(deepcopy(sim_params), values, update)):

        inst_outs = [None] * n_sims
        for s_ind in range(n_sims):
            inst_outs[s_ind] = measure_func(sim_func(**cur_sim_params), **measure_params)

        avg[sp_ind] = avg_func(inst_outs, 0)
        if var_func is not None:
            var[sp_ind] = var_func(inst_outs, 0)

    if var_func is not None:
        return avg, var
    else:
        return avg


def run_sims_parallel(sim_func, sim_params, measure_func, measure_params, update, values,
                      n_sims=10, avg_func=np.mean, var_func=None, n_jobs=-1, pbar=False):
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

    if var_func is not None:
        variability = var_func(measures, axis=1)
        return averages, variability
    else:
        return averages


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
        A collected of the simulation parameters.
        Only returned if `return_sim_params` is True.
    """

    n_measures = len(measures)

    results = {func.__name__ : deepcopy(np.zeros(n_sims)) for func in measures.keys()}

    cur_sim_params = deepcopy(sim_params)

    if return_sim_params:
        all_sim_params = []

    for s_ind in range(n_sims):

        for key, val in samplers.items():
            UPDATES[key](cur_sim_params, next(val))

        if verbose:
            print(cur_sim_params)
        if return_sim_params:
            all_sim_params.append(deepcopy(unpack_param_dict(cur_sim_params)))

        sig = sim_func(**cur_sim_params)

        for measure, params in measures.items():
            results[measure.__name__][s_ind] = measure(sig, **params)

    if return_sim_params:
        return results, pd.DataFrame(all_sim_params)
    else:
        return results


def run_measures(data, measures):
    """Compute multiple measures of interest across empirical recordings.

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
    outputs : dict
        Output measures.
        The keys are labels for each applied method.
        The values are the computed measures for each method.
    """

    # Initialize outputs
    outputs = {func.__name__ : np.zeros(data.shape[0]) for func in measures.keys()}

    # Calculate measures on data
    for ind, sig in enumerate(data):
        for measure, params in measures.items():
            outputs[measure.__name__][ind] = measure(sig, **params)

    return outputs


def compute_all_corrs(outputs, select=None, corr_func=bootstrap_corr):
    """Compute correlations across all sets of measures.

    Parameters
    ----------
    outputs : dict
        Measure results.
        Each key should be a measure name.
        Each set of values should be an array of measure results.
    select : 1d array of bool, optional
        A set of results to select for each measure to compute the correlation from.

    Returns
    -------
    all_corrs : dict
        Correlation results.
        Each key is a measure name.
        Each value is another dictionary, with the measure names and correlation results of all other measures.
    """

    methods = outputs.keys()

    all_corrs = {method : {} for method in methods}

    for m1 in methods:
        for m2 in methods:

            if m1 == m2:
                continue
            try:
                all_corrs[m2][m1]
            except KeyError:

                if select is not None:
                    d1, d2 = outputs[m1][select], outputs[m2][select]
                else:
                    d1, d2 = outputs[m1], outputs[m2]

                corrs = corr_func(d1, d2)
                all_corrs[m1][m2] = corrs
                all_corrs[m2][m1] = corrs

    return all_corrs
