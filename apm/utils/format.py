"""Utility functions for formatting outputs."""

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
