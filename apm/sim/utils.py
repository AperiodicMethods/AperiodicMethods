"""Simulation utilities."""

from itertools import count

###################################################################################################
###################################################################################################

def counter(value):
    """Counter that supports both finite and infinite ranges.

    Parameters
    ----------
    value : int or None
        Upper bound for the counter (if finite) or None (if infinite).

    Returns
    -------
    counter : range or count
        Counter object for finite (range) or infinite (count) iteration.
    """

    return range(value) if value else count()


def unpack_param_dict(params):
    """Unpack a dictionary of simulation parameters into a flattened dictionary.

    Parameters
    ----------
    params : dict
        Dictionary of simulation parameters.

    Returns
    -------
    nparams : dict
        Flattened dictionary of simulation parameters.
    """

    nparams = {}
    for key, value in params.items():
        if key == 'components':
            for key2 in params['components']:
                nparams.update(params['components'][key2])
        elif key == 'component_variances':
            for var_label, var_val in zip(['var_ap', 'var_pe'], params['component_variances']):
                nparams[var_label] = var_val
        else:
            nparams[key] = value

    return nparams
