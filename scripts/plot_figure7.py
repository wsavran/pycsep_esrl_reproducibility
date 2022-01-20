# 3rd party impoorts
import numpy as np
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

# local imports
from experiment_utilities import italy_experiment

# pycsep imports
from csep import load_catalog, load_gridded_forecast
from csep.utils.plots import plot_basemap, plot_catalog, plot_spatial_dataset, add_labels_for_publication


def main():

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

    # 1) Basemap

    Projection = ccrs.Mercator()   # Uses cartopy to define a projection
    extent = [5, 20, 34, 49]          # [min(lon), max(lon), min(lat), max(lat)]

    # Basemap can be defined using a predefined str, which can be looked up in the csep.utils.plots.plot_basemap()
    # documentation (e.g. stamen_terrain, google-satellite, ESRI_terrain, etc.)

    print('Loading Italy Forecasts')
    # Get forecasts and their properties
    ita_fores = initalize_forecasts(italy_experiment, swap_latlon=True)
    ita_region = ita_fores['werner-m1'].region
    ita_mw_bins = ita_fores['werner-m1'].get_magnitudes()

    # Filter the forecasts into a defined magnitude range
    low_bound = 5.25
    upper_bound = 5.95
    mw_ind = np.where(np.logical_and(ita_mw_bins >= low_bound, ita_mw_bins <= upper_bound))[0]

    # Post-process the forecasts into a desired value.
    # Here, we want to see the ratio between two forecasts within a given magnitude range
    rate_werner = np.sum(ita_fores['werner-m1'].data[:, mw_ind], axis=1)  # Get the cumulative rate in such range

    rate_meletti = np.sum(ita_fores['meletti'].data[:, mw_ind], axis=1)

    rate_diff = np.log10(rate_meletti/rate_werner)     # Get the fraction between both forecasts
    rate_diff_cartesian = ita_region.get_cartesian(rate_diff)  # Transform the result into a cartesian 2D array

    # Load the observation catalog
    ita_cat = load_catalog(italy_experiment.evaluation_catalog, loader=italy_experiment.catalog_loader)
    # Filter by the magnitude range
    ita_cat.filter([f'magnitude >= {low_bound}',f'magnitude <= {upper_bound}'])

    basemap = 'stamen_terrain-background'

    # Create an 'ax' object containing the basemap
    fig = plt.figure(figsize=(18,10))
    for idx in range(3):
        ax = fig.add_subplot(1, 3, idx+1, projection=ccrs.Mercator())

        # Plot basemap
        if idx >= 0:
            ax = plot_basemap(basemap, extent,
                              projection=Projection,
                              figsize=(7, 7),
                              coastline=True,
                              borders=True,
                              linewidth=0.4,
                              linecolor='gray',
                              grid=True,
                              grid_labels=True,
                              grid_fontsize=14,
                              ax=ax)

        # Plot post-processed forecasts
        if idx >= 1:

            # Define the plot arguments
            colormap_title = r'$\mathrm{log}_{10}\,\dfrac{\lambda_{\mathrm{meletti}}}{\lambda_{\mathrm{werner-m1}}},\quad' \
                             r'\forall m\in[5.55,5.95]$'
            args = {'cmap': 'coolwarm',
                    'alpha': 0.6,
                    'clim': (-2, 2),
                    'include_cbar': False,
                    'clabel': colormap_title,
                    'clabel_fontsize': 12,
                    'cticks_fontsize': 8,
                    'region_border': False,
                    'linewidth': 0.4}

            # Only include cbar on third panel
            if idx >= 2:
                args['include_cbar'] = True

            ## Plot the spatial dataset, using the previously defined basemap 'ax' as argument.
            ax = plot_spatial_dataset(rate_diff_cartesian, ita_region, ax=ax, extent=extent, plot_args=args)

        # 3) Catalog
        if idx >= 2:
            args = {'alpha': 0.5,
                    'markercolor': 'black',
                    'legend': True,
                    'legend_title': r'$M_w$',
                    'legend_loc': 4,
                    'mag_ticks': np.array([5.3, 5.6, 5.9]),
                    'legend_framealpha': 0.5,
                    'legend_fontsize' : 8,
                    'legend_titlesize' : 14,
                    'markersize': 0.5,
                    'mag_scale': 10,
                    'linewidth': 0.4}
            # Plot the catalog, using the previously obtained spatial_dataset 'ax' object as argument
            ax = plot_catalog(ita_cat, ax=ax, extent=extent, plot_args=args)
    fig.subplots_adjust(hspace=0.5)
    add_labels_for_publication(fig)
    fig.savefig('../figures/figure7.png', dpi=300)


if __name__ == "__main__":
    main()
