"""   """

import numpy as np

##########################################################################################
##########################################################################################

def load_psd(f_name):
    """   """

    # Load data
    data = np.load(f_name)

    # Unpack
    freqs = data['arr_0']
    psds = data['arr_1']
    chans = data['arr_2']

    return freqs, psds, chans

def fit_sls(freqs, psds, fn):
    """   """

    sls = []
    for psd in psds:
        sls.append(fn(freqs, psd))

    return sls
