"""Code for running simulation experiments."""

from copy import deepcopy

from multiprocessing import Pool, cpu_count
from functools import partial
from tqdm.notebook import tqdm

import numpy as np

###################################################################################################
###################################################################################################

upd_exp = lambda params, val : params.update({'exponent' : val})
upd_freq = lambda params, val : params['components']['sim_oscillation'].update({'freq' : val})
upd_pow = lambda params, val : params.update({'component_variances' : [1, val]})
upd_comb_exp = lambda params, val : params['components']['sim_powerlaw'].update({'exponent' : val})


UPDATES = {
    'update_exp' : upd_exp,
    'update_freq' : upd_freq,
    'update_pow' : upd_pow,
    'update_comb_exp' : upd_comb_exp
}


def update_vals(sim_params, values, update):
    """Update simulation parameter values."""

    for val in values:
        update(sim_params, val)
        yield sim_params


def run_sims(sim_func, sim_params, measure_func, measure_params, values, update, n_sims=10):
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
    values : list or 1d array
        A parameter to step across and re-run measure calculations for.
    update : {'update_exp', 'update_freq', 'update_pow', 'update_comb_exp'} or callable
        Specifies which parameter to update in simulation parameters.
    n_sims : int, optional, default: 10
        The number of iterations to simulate and calculate measures, per value.

    Returns
    -------
    measures : 1d array
        The results of the measures applied to the set of simulations.

    Notes
    -----
    The mean measure across `n_sims` of simulations if computed and returned.
    """

    outs = []

    update = UPDATES[update] if isinstance(update, str) else update

    for cur_sim_params in update_vals(deepcopy(sim_params), values, update):

        inst_outs = []
        for ind in range(n_sims):

            sig = sim_func(**cur_sim_params)
            inst_outs.append(measure_func(sig, **measure_params))

        outs.append(np.mean(inst_outs, 0))

    return outs


def run_sims_parralel(sim_func, sim_params, measure_func, measure_params,
                      values, update, n_sims=10, n_jobs=-1):
    """Compute a set of measures across simulations - in parallel."""

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
                             total=len(sim_params), dynamic_ncols=True))

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

    measures = np.mean(measures, axis=1)

    return measures


def _proxy(sim_params, sim_func=None, measure_func=None, measure_params=None):
    """Wrap simulation and measure functions together."""

    return measure_func(sim_func(**sim_params), **measure_params)


def run_comparisons(sim_func, sim_params, measures, samplers, n_sims, verbose=False):
    """Compute multiple measures of interest across the same set of simulations.

    Parameters
    ----------
    sim_func : callable
        A function to create simulated time series.
    sim_params : dict
        Input arguments for `sim_func`.
    measures : dict
        A measure function to apply to the simulated data.
        The keys should be functions to apply to the data.
        The values should be a dictionary of parameters to use for the method.
    samplers : dict
        Information for how to sample across parameters for the simulations.
        The keys should be string labels of which parameter to update.
        The values should be data ranges to sample for that parameter.
    n_sims : int
        The number of simulations to run.
    verbose : bool, optional, default: False
        Whether to print out simulation parameters.
        Used for checking simulations / debugging.

    Returns
    -------
    outs : dict
        Computed results for each measure across the set of simulated data.
    """

    n_measures = len(measures)

    outs = {func.__name__ : deepcopy(np.zeros(n_sims)) for func in measures.keys()}

    cur_sim_params = deepcopy(sim_params)

    for s_ind in range(n_sims):

        for key, val in samplers.items():
            UPDATES[key](cur_sim_params, next(val))

        if verbose:
            print(cur_sim_params)

        sig = sim_func(**cur_sim_params)

        for measure, params in measures.items():
            outs[measure.__name__][s_ind] = measure(sig, **params)

    return outs
