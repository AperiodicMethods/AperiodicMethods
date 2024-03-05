"""Param management.

NOTE: This code is a candidate for moving to NDSP.
"""

from copy import deepcopy

from apm.sim.params import update_vals

###################################################################################################
###################################################################################################

## PARAM UPDATERS

def param_updater(parameter):
    """Create a lambda updater function to update a specified parameter."""

    return lambda params, value : params.update({parameter : value})


def component_updater(component, parameter):
    """Create a lambda updater function to update a parameter within a simulation component."""

    return lambda params, value : params['components'][component].update({parameter : value})


## PARAM YIELDER

def param_yielder(updater, sim_params, values):
    """Parameter yielder."""

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

        self._updater = self._create_updater()
        self._reset_yielder()


    def __next__(self):
        """Sample the next set of simulation parameters."""

        return next(self.yielder)


    def __iter__(self):
        """Iterate across simulation parameters."""

        self._reset_yielder()
        for _ in range(len(self)):
            yield next(self)


    def __len__(self):
        """Define length of the object as the number of values to step across."""

        return len(self.values)


    def _create_updater(self):
        """Initialize the updater function used to update simulation parameters."""

        if self.component is not None:
            updater = component_updater(self.component, self.update)
        else:
            updater = param_updater(self.update)

        return updater


    def _reset_yielder(self):
        """Reset the object yielder."""

        self.yielder = param_yielder(self._updater, self.params, self.values)


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
    """

    def __init__(self, sim_func, sim_params, n_sims):
        """Initialize signal iteration object."""

        self.sim_func = sim_func
        self.sim_params = deepcopy(sim_params)
        self.n_sims = n_sims


    def __next__(self):
        """Sample a new simulation."""

        return self.sim_func(**self.sim_params)


    def __iter__(self):
        """Iterate across simulation outputs."""

        for _ in range(self.n_sims):
            yield next(self)


    def __len__(self):
        """Define length of the object as the number of simulations to create."""

        return self.n_sims


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
