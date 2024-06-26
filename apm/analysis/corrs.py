"""Compute and compare correlations between measures."""

from itertools import product

import numpy as np
from sklearn import linear_model

from bootstrap import bootstrap_corr, bootstrap_diff

from apm.utils.data import select_vals

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

        d1, d2 = select_vals(select, results[m1], results[m2])

        corrs = corr_func(d1, d2)
        all_corrs[m1][m2] = corrs
        all_corrs[m2][m1] = corrs

    return all_corrs


def compute_corrs_to_feature(results, feature, select=None, corr_func=bootstrap_corr):
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
    select : 1d array of bool, optional
        A set of results to select for each measure to compute the correlation from.

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

        result, feat = select_vals(select, results[method], feature)
        all_corrs[method] = corr_func(result, feat)

    return all_corrs


def compute_diffs_to_feature(results, feature, select=None, diff_func=bootstrap_diff):
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
    select : 1d array of bool, optional
        A set of results to select for each measure to compute the correlation from.

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

        feature, result1, result2 = select_vals(select, feature, results[m1], results[m2])

        diffs = diff_func(feature, result1, result2)
        all_diffs[m1][m2] = diffs
        all_diffs[m2][m1] = diffs

    return all_diffs


def unpack_corrs(corrs):
    """Unpack a correlation dictionary into a matrix.

    Parameters
    ----------
    corrs : dict
        Dictionary of correlation results.

    Returns
    -------
    corrs_mat : 2d array
        Matrix of correlation values.
    """

    corrs_mat = np.zeros([len(corrs.keys()), len(corrs.keys())])

    for ii, m1 in enumerate(corrs.keys()):
        for jj, m2 in enumerate(corrs.keys()):
            if ii == jj:
                corrs_mat[ii, jj] = np.nan
            else:
                corrs_mat[ii, jj] = corrs[m1][m2][0]

    return corrs_mat


def compute_reg_var(var, control):
    """Compute a partialized variable - residuals after removing impact of another variable."""

    vals = var.reshape(-1, 1)
    cont = control.reshape(-1, 1)

    vals_reg = linear_model.LinearRegression().fit(cont, vals)
    vals_res = vals - vals_reg.predict(cont)

    return vals_res
