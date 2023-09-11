"""Utilities for managing and updating simulation parameters."""

###################################################################################################
###################################################################################################

# Update aperiodic parameters - exponent
upd_exp = lambda params, val : params.update({'exponent' : val})

# Update aperiodic parameters (in combined signals) - exponent
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
