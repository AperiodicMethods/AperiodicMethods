"""   """

from __future__ import print_function

import numpy as np

from slf.fit import *
from slf.fake import *
from foof import syn

#########################################################################################
#########################################################################################

def main():
    """   """

    syns = SynFits()
    syns.get_fit_funcs()

    #
    n_psds = 2
    slv = 1

    fs, psds = mk_psds(n_psds, slv)

    #
    syns.fit_slopes(slv, fs, psds)
    mes = syns.calc_mean_errs()

    print_errs(mes)


if __name__ == '__main__':
    main()