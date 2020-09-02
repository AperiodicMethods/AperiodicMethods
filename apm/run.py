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


def run_sims(sim_func, sim_params, measure_func, measure_params, n_instances=10,
             values=np.arange(-3, 0.25, 0.25), update='update_exp', n_jobs=-1):
    """Run a set of calculated measures across simulations.

    sim_func : function
        A timeseries simulation function (i.e. from neurodsp.sim).
    sim_params : dict
        Arguments to be used with ``sim_func``.
    measure_func : function
        An entropy function from ``pyegg.code.entropy``.
    measure_params : dict
        Arguments to be used with ``measure_func``.
    n_instances : int, optional, default: 10
        The number of times to run simulations and measure calculations.
        The mean across these instances is taken.
    values : list or 1d array, optional, default: np.arange(-3, 0.25, 0.25)
        A parameter to step across and re-run measure calculations for.
    update : string, optional, default: 'update_exp'
        The kwarg to pair values to in ``UPDATES``.
    n_jobs : int, optional, default: -1
        The number of jobs to run in parallel. -1 defaults to maximum jobs.

    Returns
    -------
    measures : 1d array
        Entropy measure returned from ``pyegg.code.entropy``.
    """

    n_jobs = cpu_count() if n_jobs == -1 else n_jobs

    # Generator to list
    update = UPDATES[update] if isinstance(update, str) else update
    sim_params = update_vals(deepcopy(sim_params), values, update)
    sim_params = [deepcopy(next(sim_params)) for vi in values]

    # Duplicate sims to equal length of n_instances
    sim_params = [pii for pi in range(len(sim_params)) for pii in [sim_params[pi]] * n_instances]

    with Pool(processes=n_jobs) as pool:

        mapping = pool.imap(partial(_proxy, sim_func=sim_func, measure_func=measure_func,
                                    measure_params=measure_params),
                            sim_params)

        measures = list(tqdm(mapping, desc="Running Simulations",
                             total=len(sim_params), dynamic_ncols=True))

    # Rehape array and take mean across n_instances
    measures = np.array(measures)
    remainder = int(measures.size / (len(values)*n_instances))

    if remainder == 1:
        # Cases when measure_func returns a single value
        measures = np.reshape(measures, (len(values), n_instances))
    else:
        # Cases where measure_func returns >1 value
        try:
            measures = np.reshape(measures, (len(values), n_instances, remainder))
        except:
            raise ValueError('The measure function returns an array with varying shape.')

    measures = np.mean(measures, axis=1)
    return measures


def update_vals(sim_params, values, update):

    for val in values:
        update(sim_params, val)
        yield sim_params


def _proxy(sim_params, sim_func=None, measure_func=None, measure_params=None):
    """Wrap simulation and measure functions together."""

    return measure_func(sim_func(**sim_params), **measure_params)
