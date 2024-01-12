"""Compute measures on results."""

import numpy as np

###################################################################################################
###################################################################################################

def compute_avgs(results, avg_func=np.nanmean):
    """Compute averages across a set of results.

    Parameters
    ----------
    results : dict
        Dictionary of results

    Returns
    -------
    dict
        Averaged results.
    """

    return {measure : avg_func(results[measure], 0) for measure in results.keys()}
