"""Param management.

NOTE: This code is a candidate for moving to NDSP.
"""

from copy import deepcopy

from apm.sim.params import update_vals
from apm.sim.sim import sig_yielder

###################################################################################################
###################################################################################################

## PARAM UPDATERS

def param_updater(parameter):
    """Create a lambda updater function to update a specified parameter.

    Parameters
    ----------
    parameter : str
        Name of the parameter to update.

    Returns
    -------
    callable
        Updater function which can update specified parameter in simulation parameters.
    """

    return lambda params, value : params.update({parameter : value})


def component_updater(parameter, component):
    """Create a lambda updater function to update a parameter within a simulation component.

    Parameters
    ----------
    parameter : str
        Name of the parameter to update.
    component : str
        Name of the component to update the parameter within.

    Returns
    -------
    callable
        Updater function which can update specified parameter in simulation parameters.
    """

    return lambda params, value : params['components'][component].update({parameter : value})


def create_updater(update, component=None):
    """Create an updater function for updating simulation parameters.

    Parameters
    ----------
    parameter : str
        Name of the parameter to update.
    component : str
        Name of the component to update the parameter within.

    Returns
    -------
    callable
        Updater function which can update specified parameter in simulation parameters.
    """

    if component is not None:
        updater = component_updater(update, component)
    else:
        updater = param_updater(update)

    return updater


## PARAM YIELDER

def param_iter_yielder(sim_params, updater, values):
    """Parameter yielder.

    Parameters
    ----------
    sim_params : dict
        Parameter definition.
    updater : callable
        Updater function to update parameter definition.
    values : 1d array
        Values to iterate across.

    Yields
    ------
    sim_params : dict
        Simulation parameter definition.
    """

    # The deepcopy'ing ensures to not change the input dict & that each output is new
    for cur_params in update_vals(deepcopy(sim_params), values, updater):
        yield deepcopy(cur_params)


## PARAM ITER

class ParamIter():
    """Object for iterating across parameter updates.

    Parameters
    ----------
    params : dict
        Parameter definition to create iterator with.
    update : str
        Name of the parameter to update.
    values : 1d array
        Values to iterate across.
    component : str, optional
        Which component to update the parameter in.
        Only used if the parameter definition is for a multi-component simulation.

    Attributes
    ----------
    index : int
        Index of current location through the iteration.
    yielder : generator
        Generator for sampling the sig iterations.
    """

    def __init__(self, params, update, values, component=None):
        """Initialize parameter iteration object."""

        params = deepcopy(params)

        if component is not None:
            params['components'][component][update] = None
        else:
            params[update] = None

        self.params = params
        self.update = update
        self.values = values
        self.component = component

        self._updater = create_updater(self.update, self.component)

        self.index = 0
        self.yielder = None
        self._reset_yielder()


    def __next__(self):
        """Sample the next set of simulation parameters."""

        self.index += 1
        return next(self.yielder)


    def __iter__(self):
        """Iterate across simulation parameters."""

        self._reset_yielder()
        for _ in range(len(self)):
            yield next(self)


    def __len__(self):
        """Define length of the object as the number of values to step across."""

        return len(self.values)


    def _reset_yielder(self):
        """Reset the object yielder."""

        self.index = 0
        self.yielder = param_iter_yielder(self.params, self._updater, self.values)


def param_iter(params, update, values, component=None):
    """Wrapper function for the ParamIter object.

    Parameters
    ----------
    params : dict
        Parameter definition to create iterator with.
    update : str
        Name of the parameter to update.
    values : 1d array
        Values to iterate across.
    component : str, optional
        Which component to update the parameter in.
        Only used if the parameter definition is for a multi-component simulation.

    Returns
    -------
    ParamIter
        Iterable object for iterating across parameter definitions.
    """

    return ParamIter(params, update, values, component)

## SIG YIELDER / ITER

# Note: consolidate with sig_yielder

class SigIter():
    """Object for iterating across sampled simulations.

    Parameters
    ----------
    sim_func : callable
        Function to create simulations.
    sim_params : dict
        Simulation parameters.
    n_sims : int
        Number of simulations to create.

    Attributes
    ----------
    index : int
        Index of current location through the iteration.
    yielder : generator
        Generator for sampling the sig iterations.
    """

    def __init__(self, sim_func, sim_params, n_sims):
        """Initialize signal iteration object."""

        self.sim_func = sim_func
        self.sim_params = deepcopy(sim_params)
        self.n_sims = n_sims

        self.index = 0
        self.yielder = None
        self._reset_yielder()


    def __next__(self):
        """Sample a new simulation."""

        self.index += 1

        return next(self.yielder)


    def __iter__(self):
        """Iterate across simulation outputs."""

        self._reset_yielder()
        for _ in range(len(self)):
            yield next(self)


    def __len__(self):
        """Define length of the object as the number of simulations to create."""

        return self.n_sims


    def _reset_yielder(self):
        """Reset the object yielder."""

        self.index = 0
        self._yielder = sig_yielder(self.sim_func, self.sim_params, self.n_sims)


def sig_iter(sim_func, sim_params, n_sims):
    """Wrapper function for the SigIter object.

    Parameters
    ----------
    sim_func : callable
        Function to create simulations.
    sim_params : dict
        Simulation parameters.
    n_sims : int
        Number of simulations to create.

    Returns
    -------
    SigIter
        Iterable object for sampling simulatons.
    """

    return SigIter(sim_func, sim_params, n_sims)