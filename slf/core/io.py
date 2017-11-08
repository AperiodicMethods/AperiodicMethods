"""I/O utilities for slf."""

import os
import pickle

##########################################################################################
##########################################################################################

def save_pickle(dat, f_name, save_path):
	"""Save a data object to a pickle file."""

	with open(os.path.join(save_path, f_name), 'wb') as pickle_file:
		pickle.dump(dat, pickle_file)


def load_pickle(f_name, save_path):
	"""Load a data objcet from a pickle file."""

	with open(os.path.join(save_path, f_name), 'rb') as pickle_file:
		dat = pickle.load(pickle_file)

	return dat