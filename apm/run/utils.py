"""Utilities for helping with running measures."""

###################################################################################################
###################################################################################################

def set_measure_settings(measures, setting, value):
    """Set measure settings in a measures dictionary.

    Parameters
    ----------
    measures : dict
        Dictionary of measures, with keys as functions, and values as settings dictionaries.
    setting : str
        The settings to check for an update throughout `measures`.
    value : obj
        The value to set the setting to.

    Returns
    -------
    measures : dict
        Update measures dictionary.
    """

    for func, settings in measures.items():
        for key in settings.keys():
            if key == setting:
                measures[func][key] = value

    return measures


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
