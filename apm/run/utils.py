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
        for key, val in settings.items():
            if key == setting:
                measures[func][key] = value
