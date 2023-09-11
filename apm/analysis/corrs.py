"""Compute and compare correlations between measures."""

from itertools import product

from bootstrap import bootstrap_corr, bootstrap_diff

###################################################################################################
###################################################################################################

def compute_all_corrs(results, select=None, corr_func=bootstrap_corr):
    """Compute correlations across all sets of measures.

    Parameters
    ----------
    results : dict
        Measure results.
        Each key should be a measure name.
        Each set of values should be an array of measure results.
    select : 1d array of bool, optional
        A set of results to select for each measure to compute the correlation from.

    Returns
    -------
    all_corrs : dict
        Correlation results.
        Each key is a measure name.
        Each value is another dictionary, with names & correlation results of all other measures.
    """

    methods = results.keys()
    all_corrs = {method : {} for method in methods}

    for m1, m2 in product(methods, methods):

        # Skip if m's are same, or if results already in output
        if m1 == m2 or all_corrs.get(m2).get(m1) is not None:
            continue

        if select is not None:
            d1, d2 = results[m1][select], results[m2][select]
        else:
            d1, d2 = results[m1], results[m2]

        corrs = corr_func(d1, d2)
        all_corrs[m1][m2] = corrs
        all_corrs[m2][m1] = corrs

    return all_corrs


def compute_corrs_to_feature(results, feature, corr_func=bootstrap_corr):
    """Compute correlations between a set of measures and a given feature.

    Parameters
    ----------
    results : dict
        Measure results.
        Each key should be a measure name.
        Each set of values should be an array of measure results.
    feature : 1d array
        Vector of values to computer correlations to.
        Should have the same length as each entry in `results`.

    Returns
    -------
    all_corrs : dict
        Correlation results.
        Each key is a measure name.
        Each value is the correlation results between this measure and the given feature.
    """

    methods = results.keys()

    all_corrs = {method : None for method in methods}

    for method in methods:
        all_corrs[method] = corr_func(results[method], feature)

    return all_corrs


def compute_diffs_to_feature(results, feature, diff_func=bootstrap_diff):
    """Compute differences between correlations of a set of measures to a given feature.

    Parameters
    ----------
    results : dict
        Measure results.
        Each key should be a measure name.
        Each set of values should be an array of measure results.
    feature : 1d array
        Vector of values to computer correlations to.
        Should have the same length as each entry in `results`.

    Results
    -------
    all_diffs : dict
        Difference results.
        Each key is a measure name.
        Each value is another dictionary, with names & correlation results of all other measures.
    """

    methods = results.keys()
    all_diffs = {method : {} for method in methods}

    for m1, m2 in product(methods, methods):

        # Skip if m's are same, or if results already in output
        if m1 == m2 or all_diffs.get(m2).get(m1) is not None:
            continue

        diffs = diff_func(feature, results[m1], results[m2])
        all_diffs[m1][m2] = diffs
        all_diffs[m2][m1] = diffs

    return all_diffs
