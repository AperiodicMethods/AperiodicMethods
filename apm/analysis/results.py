"""Compute measures on results."""

from math import sqrt
from statistics import mean, stdev

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


def cohens_d(d1, d2):
    """Compute Cohen's D effect size measure between two sets of results."""

    return (mean(d1) - mean(d2)) / (sqrt((stdev(d1) ** 2 + stdev(d2) ** 2) / 2))
