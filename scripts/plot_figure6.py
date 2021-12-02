# Python imports
import time

# 3rd party impoorts
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

# pycsep imports
from csep import load_gridded_forecast, load_catalog
from csep import poisson_evaluations as poisson
from csep.utils.plots import plot_comparison_test, add_labels_for_publication

# local imports
from experiment_utilities import california_experiment, italy_experiment


def initalize_forecasts(config, **kwargs):
    """ Initialize forecast using experiment configuration """
    out = {}
    for name, path in config.forecasts.items():
        print(f'Loading {name} forecast...')
        fore = load_gridded_forecast(path, **kwargs)
        fore.start_time = config.start_time
        fore.end_time = config.end_time
        fore.name = name
        out[name] = fore
    return out

def main():

	# evaluate california_experiment using helmstetter as benchmark
	california_t_results = []
	california_w_results = []
	cat = load_catalog(
	    california_experiment.evaluation_catalog,
	    loader=california_experiment.catalog_loader,
	)
	print(cat)

	# load forecasts and store benchmark forecast
	ca_fores = initalize_forecasts(california_experiment)
	benchmark = ca_fores.pop(california_experiment.t_test_benchmark)

	print(f'Computing t-test results...')
	for name, fore in ca_fores.items():
	    fore.name = fore.name.upper()
	    california_t_results.append(poisson.paired_t_test(fore, benchmark, cat))
	    california_w_results.append(poisson.w_test(fore, benchmark, cat))

	# evaluate italy_experiment
	italy_t_results = []
	italy_w_results = []
	cat = load_catalog(
	    italy_experiment.evaluation_catalog,
	    loader=italy_experiment.catalog_loader,
	)

	# load forecasts and store benchmark forecast
	ita_fores = initalize_forecasts(italy_experiment, swap_latlon=True)
	benchmark = ita_fores.pop(italy_experiment.t_test_benchmark)

	# italian catalog needs to be filtered in magnitude for 5yr forecasts
	cat.filter(f'magnitude >= {benchmark.min_magnitude}')
	print(cat)

	print(f'Computing t-test results...')
	for name, fore in ita_fores.items():
	    fore.name = fore.name.upper()
	    italy_t_results.append(poisson.paired_t_test(fore, benchmark, cat))
	    italy_w_results.append(poisson.w_test(fore, benchmark, cat))

	# plotting code below
	fig, (ax1, ax2) = plt.subplots(1,2, figsize=(12,5))
	args = {
	    'figsize':(6,8),
	    'xlabel': '',
	    'linewidth': 1.5,
	    'capsize': 0,
	    'title': '',
	    'xlabel_fontsize': 12,
	    'ylabel_fontsize': 14,
	    'ylabel': 'Information Gain per Eq.',
	    'markersize': 6,
	    'xlim': [-0.5, 1.5],
	    'xticklabels_rotation': 45
	}

	ax1 = plot_comparison_test(california_t_results, california_w_results, plot_args=args, axes=ax1)

	# args['ylabel'] = ''
	ax2 = plot_comparison_test(italy_t_results, italy_w_results, plot_args=args, axes=ax2)
	add_labels_for_publication(fig)
	fig.tight_layout()
	fig.savefig('./figures/figure6.png', dpi=300)

if __name__ == "__main__":
	main()


