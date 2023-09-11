"""Compute and compare error metrics of aperiodic methods."""

###################################################################################################
###################################################################################################

def abs_err(val, fit):
    """Absolute error of fit."""

    return abs(val - fit)


def sqd_err(val, fit):
    """Squared error of fit."""

    return (val - fit) ** 2
