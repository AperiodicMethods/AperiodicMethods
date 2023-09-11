"""Utilities for aperiodic methods project."""

import numpy as np

###################################################################################################
###################################################################################################

def CheckDims1D(func):
    """Decorator function to check all inputs are 1-D."""

    def wrapper(*args):
        args = [_check1D(arg) for arg in args]
        return func(*args)

    return wrapper

def CheckDims2D(func):
    """Decorator function to check all inputs are 2-D."""

    def wrapper(*args):
        args = [_check2D(arg) for arg in args]
        return func(*args)

    return wrapper


def _check1D(arr):
    """Check that array is 1-D, squeeze if not."""

    if arr.ndim == 2:
        return np.squeeze(arr)
    else:
        return arr

def _check2D(arr):
    """Check that array is 2-D, reshape if not."""

    if arr.ndim == 1:
        return arr.reshape([len(arr), 1])
    else:
        return arr
