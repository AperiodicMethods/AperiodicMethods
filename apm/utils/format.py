"""Utility functions for formatting outputs."""

from itertools import combinations

from apm.plts.settings import ABBRS

###################################################################################################
###################################################################################################

def print_results(data):
    """Print out the mean errors per method.

    Parameters
    ----------
    data : list of tuple
        List with each element containing (float, string).
    """

    for it in data:
        print('   {:8} \t\t {:1.5f}'.format(it[1], it[0]))


def format_corr(r_val, p_val, cis):
    """Format correlation results for printing."""

    return 'r={:+1.3f}  CI[{:+1.3f}, {:+1.3f}],  p={:1.3f}'.format(r_val, *cis, p_val)


def print_all_corrs(corrs, rows, columns):
    """Print out a set of correlations defined as a two-dimensional sweep."""

    print('Correlations:')
    for row in rows:
        for col in columns:
            print('  {:6s} & {:6s}:  '.format(ABBRS[row], ABBRS[col]),
                  format_corr(*corrs[row][col]))


def print_corr_combs(corrs, combs=None):
    """Print correlations, stepping through all combinations."""

    if not combs:
        combs = list(corrs.keys())

    print('Correlations:')
    for comb in combinations(combs, 2):
        print('  {:6s} & {:6s}:  '.format(ABBRS[comb[0]], ABBRS[comb[1]]),
              format_corr(*corrs[comb[0]][comb[1]]))
