"""Code for running simulation experiments."""

import warnings
from copy import deepcopy
from functools import partial
from multiprocessing import Pool, cpu_count

import numpy as np
import pandas as pd
from tqdm.notebook import tqdm

from neurodsp.sim.io import load_sims
from neurodsp.sim.multi import sig_yielder, sig_sampler

from apm.io.db import APMDB
from apm.run.utils import unpack_param_dict

###################################################################################################
###################################################################################################

def run_sims(sim_func, sim_params, measure_func, measure_params, n_sims,
             return_params=False, outsize=1, warnings_action='ignore'):
    """Compute a measure of interest across a set of simulations.

    Parameters
    ----------
    sim_func : callable
        A function to create the simulations from.
    sim_params : iterable or list of dict
        Simulation parameters for `sim_func`.
    measure_func : callable
        A measure function to apply to the simulated data.
    measure_params : dict
        Input arguments for `measure_func`.
    n_sims : int
        The number of iterations to simulate and calculate measures, per value.
    return_params : bool, default: False
        Whether to collect and return the parameters for the generated simulations.
    outsize : int, optional, default: 1
        Expected size of the measure results.
    warnings_action : {'ignore', 'error', 'always', 'default', 'module, 'once'}
        Filter action for warnings.

    Returns
    -------
    measures : 1d array
        The results of the measures applied to the set of simulations.
    """

    results = np.zeros([len(sim_params), n_sims, outsize]) if outsize > 1 \
        else np.zeros([len(sim_params), n_sims])

    if return_params:
        all_sim_params = []

    with warnings.catch_warnings():
        warnings.simplefilter(warnings_action)

        for p_ind, cur_sim_params in enumerate(sim_params):

            if return_params:
                all_sim_params.append(deepcopy(cur_sim_params))

            for s_ind, sig in enumerate(sig_yielder(sim_func, cur_sim_params, n_sims)):
                results[p_ind, s_ind] = measure_func(sig, **measure_params)

    if return_params:
        return results, all_sim_params
    else:
        return results


def run_sims_load(sims_file, measure_func, measure_params, n_sims=None,
                  outsize=1, warnings_action='ignore'):
    """Run measures across a set of simulations loaded from file.

    Notes
    -----
    This function has the same call signature as `run_sims`,
    replacing `sims_files` for sim_func, sim_params.
    """

    # Load saved out simulations file and collect info of interest
    sigs = load_sims(sims_file, APMDB().sims_path / 'time_series')
    values = sigs.values
    n_sets = len(sigs)
    n_params = len(values)

    if n_sims:
        for el in range(n_sets):
            sigs[el].signals = sigs[el].signals[:n_sims, :]
    n_sims = len(sigs[0])

    results = np.zeros([n_params, n_sims, outsize]) if outsize > 1 \
        else np.zeros([n_params, n_sims])

    with warnings.catch_warnings():
        warnings.simplefilter(warnings_action)

        for sp_ind, value in enumerate(values):

            for s_ind, sig in enumerate(sigs[sp_ind]):
                results[sp_ind, s_ind] = measure_func(sig, **measure_params)

    return results


def run_sims_parallel(sim_func, sim_params, measure_func, measure_params, n_sims,
                      n_jobs=4, pbar=False, warnings_action='ignore'):
    """Compute a set of measures across simulations, in parallel.

    Notes
    -----
    This function has the same call signature as `run_sims`, with the addition of `n_jobs`.
    """

    n_jobs = cpu_count() if n_jobs == -1 else n_jobs

    # Typecast generator to list & get the set of iterated values
    sim_params = list(sim_params)
    values = sim_params.values if hasattr(sim_params, 'values') \
        else list(range(len(sim_params)))

    # Duplicate sims to equal length of n_sims
    sim_params = [pii for pi in range(len(sim_params)) for pii in [sim_params[pi]] * n_sims]

    with warnings.catch_warnings():
        warnings.simplefilter(warnings_action)
        with Pool(processes=n_jobs) as pool:

            mapping = pool.imap(partial(_proxy, sim_func=sim_func, measure_func=measure_func,
                                        measure_params=measure_params), sim_params)

            results = list(tqdm(mapping, desc="Running Simulations",
                                total=len(sim_params), dynamic_ncols=True, disable=not pbar))

    results = np.array(results)
    remainder = int(results.size / (len(values) * n_sims))

    if remainder == 1:
        # Cases when measure_func returns a single value
        results = np.reshape(results, (len(values), n_sims))
    else:
        # Cases where measure_func returns >1 value
        try:
            results = np.reshape(results, (len(values), n_sims, remainder))
        except:
            raise ValueError('The measure function returns an array with varying shape.')

    return results


def _proxy(sim_params, sim_func=None, measure_func=None, measure_params=None):
    """Wrap simulation and measure functions together."""

    return measure_func(sim_func(**sim_params), **measure_params)


def run_comparisons(sim_func, sim_params, measures, n_sims=None,
                    return_params=False, verbose=False, warnings_action='ignore'):
    """Compute multiple measures of interest across the same set of simulations.

    Parameters
    ----------
    sim_func : callable
        A function to create simulated time series.
    sim_params : iterable or list of dict
        Simulation parameters for `sim_func`.
    measures : dict
        Functions to apply to the simulated data.
        The keys should be functions to apply to the data.
        The values should be a dictionary of parameters to use for the method.
    n_sims : int, optional
        The number of simulations to run.
    return_params : bool, default: False
        Whether to collect and return the parameters of all the generated simulations.
    verbose : bool, optional, default: False
        Whether to print out simulation parameters.
        Used for checking simulations / debugging.
    warnings_action : {'ignore', 'error', 'always', 'default', 'module, 'once'}
        Filter action for warnings.

    Returns
    -------
    results : dict
        Computed results for each measure across the set of simulated data.
    all_sim_params : pd.DataFrame
        Collected simulation parameters across all the simulations.
        Only returned if `return_params` is True.
    """

    if not n_sims:
        n_sims = len(sim_params)

    results = {func.__name__ : deepcopy(np.zeros(n_sims)) for func in measures.keys()}

    if return_params:
        all_sim_params = [None] * n_sims

    with warnings.catch_warnings():
        warnings.simplefilter(warnings_action)

        for s_ind, (sig, sample_params) in \
            enumerate(sig_sampler(sim_func, sim_params, True, n_sims)):

            if verbose:
                print(sample_params)

            if return_params:
                all_sim_params[s_ind] = unpack_param_dict(sample_params)

            for measure, params in measures.items():
                results[measure.__name__][s_ind] = measure(sig, **params)

    if return_params:
        all_sim_params = pd.DataFrame(all_sim_params)
        # If relevant, set a marker for yes / no if signal has an oscillation
        if 'var_pe' in all_sim_params.columns:
            all_sim_params['has_osc'] = all_sim_params['var_pe'] != 0.
        return results, all_sim_params
    else:
        return results
