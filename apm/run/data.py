"""Code for running estimates on empirical data."""

import warnings

import numpy as np

###################################################################################################
###################################################################################################

def run_measures(data, measures, warnings_action='ignore'):
    """Compute multiple measures on empirical recordings - 2D array input.

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
    results : dict
        Output measures.
        The keys are labels for each applied method.
        The values are the computed measures for each method.
    """

    results = {func.__name__ : np.zeros(data.shape[0]) for func in measures.keys()}

    with warnings.catch_warnings():
        warnings.simplefilter(warnings_action)
        for ind, sig in enumerate(data):
            for measure, params in measures.items():
                results[measure.__name__][ind] = measure(sig, **params)

    return results


def run_group_measures(group_data, measures, warnings_action='ignore'):
    """Compute multiple measures on empirical recordings - 3D array input.

    Parameters
    ----------
    group_data : 3d array
        Data to run measures on, organized as [subjects, channels, timepoints].
    measures : dict
        Functions to apply to the data.
        The keys should be functions to apply to the data.
        The values should be a dictionary of parameters to use for the method.
    """

    n_subjs, n_chs, n_timepoints = group_data.shape
    group_results = {func.__name__ : np.zeros([n_subjs, n_chs]) for func in measures.keys()}

    for ind in range(n_subjs):
        subj_measures = run_measures(np.squeeze(group_data[ind, :, :]), measures, warnings_action)
        for label in subj_measures:
            group_results[label][ind, :] = subj_measures[label]

    return group_results
