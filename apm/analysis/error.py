"""Compute and compare error metrics of aperiodic methods."""

###################################################################################################
###################################################################################################

def abs_err(measured_value, true_value):
    """Absolute error of fit."""

    return abs(measured_value - true_value)


def sqd_err(val, true_value):
    """Squared error of fit."""

    return (measured_value - true_value) ** 2


def calculate_errors(measures, true_values, error_func=abs_err):
    """Calculate errors of measured values."""

    errors = {}
    for method in measures.keys():
        errors[method] = error_func(measures[method], true_values)

    return errors
