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


def run_sims(sim_func, sim_params, measure_func, measure_params, n_instances=10,
             values=np.arange(-3, 0.25, 0.25), update='update_exp'):
    """Compute a set of measures across simulations.

    Parameters
    ----------
    sim_func : callable
        A simulation function to create the simulations from.
    sim_params : dict
        Input arguments for `sim_func`.
    measure_func : callable
        A measure function to apply to the simulatied data.
    measure_params : dict
        Input arguments for `measure_func`.
    n_instances : int, optional, default: 10
        The number of times to run simulations and measure calculations.
    values : list or 1d array, optional, default: np.arange(-3, 0.25, 0.25)
        A parameter to step across and re-run measure calculations for.
    update : {'update_exp', 'update_freq', 'update_pow', 'update_comb_exp'}
        Specifies which parameter to update in simulation parameters.

    Returns
    -------
    measures : 1d array
        The results of the measures applied to the set of simulations.

    Notes
    -----
    The mean measure across `n_instances` of simulations if computed and returned.
    """

    outs = []

    update = UPDATES[update] if isinstance(update, str) else update

    for cur_sim_params in update_vals(deepcopy(sim_params), values, update):

        inst_outs = []
        for ind in range(n_instances):

            sig = sim_func(**cur_sim_params)
            inst_outs.append(measure_func(sig, **measure_params))

        outs.append(np.mean(inst_outs, 0))

    return outs


def run_sims_parralel(sim_func, sim_params, measure_func, measure_params, n_instances=10,
                      values=np.arange(-3, 0.25, 0.25), update='update_exp', n_jobs=-1):
    """Compute a set of measures across simulations - in parallel."""

    n_jobs = cpu_count() if n_jobs == -1 else n_jobs

    # Generator to list
    update = UPDATES[update] if isinstance(update, str) else update
    sim_params = update_vals(deepcopy(sim_params), values, update)
    sim_params = [deepcopy(next(sim_params)) for vi in values]

    # Duplicate sims to equal length of n_instances
    sim_params = [pii for pi in range(len(sim_params)) for pii in [sim_params[pi]] * n_instances]

    with Pool(processes=n_jobs) as pool:

        mapping = pool.imap(partial(_proxy, sim_func=sim_func, measure_func=measure_func,
                                    measure_params=measure_params), sim_params)

        measures = list(tqdm(mapping, desc="Running Simulations",
                             total=len(sim_params), dynamic_ncols=True))

    # Rehape array and take mean across n_instances
    measures = np.array(measures)
    remainder = int(measures.size / (len(values) * n_instances))

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


def _proxy(sim_params, sim_func=None, measure_func=None, measure_params=None):
    """Wrap simulation and measure functions together."""

    return measure_func(sim_func(**sim_params), **measure_params)
