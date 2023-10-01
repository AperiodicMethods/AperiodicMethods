"""I/O utilities for the aperiodic methods project."""

import os
import pickle

import numpy as np
from scipy.io import loadmat

from apm.io.utils import clean_files, check_folder, check_ext

###################################################################################################
###################################################################################################

def get_files(path, select=None, drop_hidden=True):
    """Get a list of files from a specified directory."""

    files = sorted(os.listdir(path))

    if select:
        files = [file for file in files if select in file]

    if drop_hidden:
        files = clean_files(files)

    return files


def save_pickle(data, f_name, save_path):
    """Save a data object to a pickle file."""

    with open(check_folder(check_ext(f_name, '.p'), save_path), 'wb') as pickle_file:
        pickle.dump(data, pickle_file)


def load_pickle(f_name, save_path):
    """Load a data object from a pickle file."""

    with open(check_folder(check_ext(f_name, '.p'), save_path), 'rb') as pickle_file:
        data = pickle.load(pickle_file)

    return data


def load_eeg_demo_data(files, folder, data_field):
    """Helper function for loading the EEG demo dataset."""

    data = []
    for file in files:
        loaded = loadmat(check_folder(file, folder), squeeze_me=True)
        data.append(loaded[data_field])
    data = np.array(data)

    return data
