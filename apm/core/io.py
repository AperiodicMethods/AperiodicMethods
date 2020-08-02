"""I/O utilities for the aperiodic methods project."""

import os
import pickle

###################################################################################################
###################################################################################################

def save_pickle(data, f_name, save_path):
	"""Save a data object to a pickle file."""

	with open(os.path.join(save_path, f_name), 'wb') as pickle_file:
		pickle.dump(data, pickle_file)


def load_pickle(f_name, save_path):
	"""Load a data object from a pickle file."""

	with open(os.path.join(save_path, f_name), 'rb') as pickle_file:
		data = pickle.load(pickle_file)

	return data
