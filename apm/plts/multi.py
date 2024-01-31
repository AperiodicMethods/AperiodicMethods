"""Multi panel / axis plots."""

import warnings

from matplotlib import cm

from neurodsp.plts.utils import savefig

from apm.plts.utils import make_axes
from apm.plts.results import plot_topo
from apm.plts.base import plot_dots
from apm.plts.settings import LABELS

###################################################################################################
###################################################################################################

@savefig
def plot_results_all(results, labels=None, **plt_kwargs):
    """Plot multi-axis figure comparing all measures to each other.

    Parameters
    ----------
    results : dict
        Results.
    labels : list of str, optional
        Set of measures in results to plot.
        If not provided, plots all measures in results.
    """

    if not labels:
        labels = list(results.keys())

    n_measures = len(labels)

    plt_kwargs.setdefault('alpha', 0.75)

    axes = make_axes(n_measures, n_measures, figsize=(24, 24), wspace=0.1, hspace=0.1)

    for ax_r, l1 in enumerate(labels):
        for ax_c, l2 in enumerate(labels):

            if ax_r <= ax_c:
                axes[ax_r, ax_c].axis('off')
                continue

            with warnings.catch_warnings():
                warnings.simplefilter('ignore')

                ax_kwargs = {}
                if ax_r != (n_measures) - 1:
                    ax_kwargs['xticks'] = []
                else:
                    ax_kwargs['xlabel'] = LABELS[l2]
                if ax_c != 0:
                    ax_kwargs['yticks'] = []
                else:
                    ax_kwargs['ylabel'] = LABELS[l1]

                plot_dots(results[l2], results[l1], **ax_kwargs,
                          **plt_kwargs, ax=axes[ax_r, ax_c])


@savefig
def plot_topo_row(results, measures, info, **plt_kwargs):
    """Helper function to plot a row of topographies."""

    axes = make_axes(1, len(measures), figsize=(2.5 * len(measures), 3),
                     wspace=plt_kwargs.pop('wspace', 0.35))
    for measure, ax in zip(measures, axes):
        ax.set_title(measure, fontdict={'fontsize' : 10})
        plot_topo(results[measure], info, axes=ax)
