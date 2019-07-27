"""
Module containing the fiex train/test split.
"""
import argparse
import numpy as np
import os
from sklearn.model_selection import train_test_split


def split_train_test(data, arrs_path, seed=0):
	"""Function to split arrays in data dictionary.

	Parameters
	----------
	data: str
		Path to data directory.

	arrs_path: str
		Array dictionary name.

	seed: int
		FIXED SEED, this is for reproducibility purposes, do not change!
	"""
	arrs = np.load(os.path.join(data, arrs_path)).item()
	assert 'X' in arrs.keys()

	X_train, X_test, Y_train, Y_test, LOS_train, LOS_test, paths_train, paths_test \
		= train_test_split(arrs['X'], arrs['Y'], arrs['LOS'], arrs['paths'],
						   test_size=0.1, stratify=arrs['Y'], random_state=seed)

	for k in list(arrs.keys()):
		arrs[k+'_train'] = eval(k+'_train')
		arrs[k+'_test'] = eval(k+'_test')
		del arrs[k]

	np.save(os.path.join(data, arrs_path), arrs)


def main():
	parser = argparse.ArgumentParser(description='Google RNN model training.')
	parser.add_argument('data', type=str, default='data/',
						help='path to save the final model')
	parser.add_argument('-t', '--t-hours', type=int,
						default=48,
						help='Maximum number of hours to allow in timeseries.')
	parser.add_argument('-n', '--n-bins', type=int,
						default=20,
						help='Number of percentile bins.')
	parser.add_argument('--seed', type=int, default=0,
						help='seed for data split')
	args = parser.parse_args()

	split_train_test(args.data,
					 arrs_path=f'arrs_{args.t_hours}_{args.n_bins}.npy',
					 seed=args.seed)


if __name__ == '__main__':
	main()
