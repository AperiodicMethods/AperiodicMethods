"""Multi panel / axis plots."""

import warnings

import numpy as np

from neurodsp.plts.utils import savefig
from neurodsp.plts.utils import make_axes

from apm.plts.results import plot_topo
from apm.plts.base import plot_dots
from apm.plts.settings import LABELS

###################################################################################################
###################################################################################################

@savefig
def plot_results_rows(results, rows, columns, tposition='tr', **plt_kwargs):
    """Plot result comparisons, organized by rows and columns.

    Parameters
    ----------
    results : Dict
        Results, organized as {label : array_of_results}.
    rows, columns : list of str
        Which results to plot across the rows and columns.
    tposition : str or array, optional
        Position to place text, to report the correlation results.
    """

    n_rows, n_cols = len(rows), len(columns)
    axes = make_axes(n_rows, n_cols,
                     figsize=plt_kwargs.pop('figsize', (4 * n_cols, 4 * n_rows)),
                     wspace=plt_kwargs.pop('wspace', 0.2),
                     hspace=plt_kwargs.pop('wspace', 0.2))
    axes = np.atleast_2d(axes).T if n_rows > n_cols else np.atleast_2d(axes)

    for ri, row in enumerate(rows):
        for ci, col in enumerate(columns):
            tpos = tposition[ri, ci] if isinstance(tposition, np.ndarray) else tposition
            plot_dots(results[row], results[col],
                      xlabel=LABELS[row], ylabel=LABELS[col],
                      tposition=tpos, **plt_kwargs, ax=axes[ri, ci])


@savefig
def plot_results_all(results, labels=None, tposition='tr', **plt_kwargs):
    """Plot multi-axis figure comparing all measures to each other.

    Parameters
    ----------
    results : dict
        Results, organized as {label : array_of_results}..
    labels : list of str, optional
        Set of measures in results to plot.
        If not provided, plots all measures in results.
    tposition : str or array, optional
        Position to place text, to report the correlation results.
    """

    if not labels:
        labels = list(results.keys())

    n_measures = len(labels) - 1

    plt_kwargs.setdefault('alpha', 0.75)

    axes = make_axes(n_measures, n_measures,
                     figsize=plt_kwargs.pop('figsize', (24, 24)),
                     wspace=plt_kwargs.pop('wspace', 0.2),
                     hspace=plt_kwargs.pop('hspace', 0.2))

    for ri, row in enumerate(labels[1:]):
        for ci, col in enumerate(labels[:-1]):

            if ri < ci:
                axes[ri, ci].axis('off')
                continue

            with warnings.catch_warnings():
                warnings.simplefilter('ignore')

                ax_kwargs = {}
                if ri != (n_measures) - 1:
                    ax_kwargs['xticks'] = []
                else:
                    ax_kwargs['xlabel'] = LABELS[col]
                if ci != 0:
                    ax_kwargs['yticks'] = []
                else:
                    ax_kwargs['ylabel'] = LABELS[row]

                tpos = tposition[ri, ci] if isinstance(tposition, np.ndarray) else tposition
                plot_dots(results[col], results[row], tposition=tpos,
                          **ax_kwargs, **plt_kwargs, ax=axes[ri, ci])


@savefig
def plot_topo_row(results, measures, info, **plt_kwargs):
    """Helper function to plot a row of topographies."""

    axes = make_axes(1, len(measures), figsize=(2.5 * len(measures), 3),
                     wspace=plt_kwargs.pop('wspace', 0.35))
    for measure, ax in zip(measures, axes):
        ax.set_title(measure, fontdict={'fontsize' : 10})
        plot_topo(results[measure], info, axes=ax)
