import time

# 3rd party impoorts
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

# pycsep imports
from csep import load_gridded_forecast, load_catalog
from csep.utils.plots import add_labels_for_publication

# local imports
from experiment_utilities import california_experiment, italy_experiment

def main():

    fig = plt.figure(figsize=(18,10))
    ax1 = fig.add_subplot(121, projection=ccrs.Mercator())
    ax2 = fig.add_subplot(122, projection=ccrs.Mercator())
    fig.subplots_adjust(wspace=0.3)

    # Load Italian forecast and catalog
    t0 = time.time()
    print('Loading Meletti forecast...')
    ita_fore = load_gridded_forecast(
        italy_experiment.forecasts['meletti'],
        swap_latlon = True
    )
    ita_fore.start_time = italy_experiment.start_time
    ita_fore.end_time = italy_experiment.end_time
    t1  = time.time()
    print(f'Loaded Meletti forecast in {t1-t0:.3f} seconds')

    print('Loading evaluation catalog for Meletti forecast...')
    ita_cat = load_catalog(
        italy_experiment.evaluation_catalog,
        loader=italy_experiment.catalog_loader,
    ).filter(f'magnitude >= {ita_fore.min_magnitude}')
    print(ita_cat)
    ita_cat.region = ita_fore.region
    t2 = time.time()
    print(f'Loaded catalog in {t2-t1:.3f} seconds')

    # Load California forecast and catalog
    print('Loading Helmstetter forecast for California...')
    ca_fore = load_gridded_forecast(california_experiment.forecasts['helmstetter'])
    ca_fore.start_time = california_experiment.start_time
    ca_fore.end_time = california_experiment.end_time
    t3 = time.time()
    print(f'Loaded Helmstetter forecast in {t3-t2:.3f} seconds')

    print('Loading evaluation catalog for Helmstetter forecast...')
    ca_cat = load_catalog(
        california_experiment.evaluation_catalog,
        loader=california_experiment.catalog_loader
    )
    print(ca_cat)
    ca_cat.region = ca_fore.region
    t4 = time.time()
    print(f'Loaded catalog in {t4-t3:.3f} seconds')

    # Plotting commands below here
    print('Plotting...')
    args_dict = {
        'basemap': 'ESRI_terrain',
        'grid_labels': True,
        'clabel': None,
        'borders': True,
        'feature_lw': 0.5,
        'cmap': 'viridis',
        'clim': [-4, 0],
        'projection': 'fast',
        'markersize': 2,
        'markercolor': 'red',
        'grid_fontsize': 14,
        'alpha': 0.9,
        'mag_scale': 7.7,
        'clabel_fontsize': 14,
        'legend_borderpad': 0.7,
        'legend_titlesize': 14,
        'legend_fontsize': 14,
        'legend': True,
        'legend_loc': 3
    }
    ax1 = ca_fore.plot(ax=ax1, plot_args=args_dict)
    args_dict['alpha'] = 0.5
    ax1 = ca_cat.plot(ax=ax1, plot_args=args_dict)
    ax1.set_title('')


    args_dict = {
        'basemap': 'ESRI_terrain',
        'grid_labels': True,
        'borders': True,
        'feature_lw': 0.5,
        'cmap': 'viridis',
        'clim': [-4, 0],
        'projection': 'fast',
        'markersize': 2,
        'markercolor': 'red',
        'grid_fontsize': 14,
        'alpha': 0.9,
        'clabel_fontsize': 14,
        'mag_scale': 8,
        'legend_fontsize': 14,
        'legend_titlesize': 14,
        'legend': True,
        'legend_loc': 3
    }
    ax2 = ita_fore.plot(ax=ax2, plot_args=args_dict)
    args_dict['alpha'] = 0.5
    ax2 = ita_cat.plot(ax=ax2, plot_args=args_dict)
    ax2.set_title('')
    add_labels_for_publication(fig)
    fig.savefig('../figures/figure2.png', dpi=300)


if __name__ == "__main__":
    main()
