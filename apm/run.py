"""Code for running simulation experiments."""

from copy import deepcopy

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

    for val in values:
        update(sim_params, val)
        yield sim_params


def run_sims(sim_func, sim_params, measure_func, measure_params, n_instances=10,
             values=np.arange(-3, 0.25, 0.25), update='update_exponent'):
    """Run a set of calculated measures across simulations."""

    outs = []

    update = UPDATES[update] if isinstance(update, str) else update

    for cur_sim_params in update_vals(deepcopy(sim_params), values, update):

        inst_outs = []
        for ind in range(n_instances):

            sig = sim_func(**cur_sim_params)
            inst_outs.append(measure_func(sig, **measure_params))

        outs.append(np.mean(inst_outs, 0))

    return outs
