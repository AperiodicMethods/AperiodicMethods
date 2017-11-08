"""Plots for the distributions of errors from slope fitting methods."""

import pandas as pd
import matplotlib.pyplot as plt

####################################################################################################
####################################################################################################

def boxplot_errors(err_dists):
	"""Plot a boxplot of distributions of errors for each slope fit method.

	Parameters
	----------
	err_dists : dict
		Dictionary of error distributions, from SynFits object.
	"""

	fig = plt.figure(figsize=[10, 5])
	plt.boxplot([err_dists[meth] for meth in err_dists.keys()],
	                labels=err_dists.keys(),
	                showfliers=False);

def violin_errors(err_dists):
	"""Plot a violin plot of distributions of errors for each slope fit method.

	Parameters
	----------
	err_dists : dict
		Dictionary of error distributions, from SynFits object.
	"""

	import seaborn as sns

	# Violin plot of the error distributions
	df = pd.DataFrame(err_dists)
	plt.figure(figsize=[16, 6])
	ax = sns.violinplot(data=df, cut=0)