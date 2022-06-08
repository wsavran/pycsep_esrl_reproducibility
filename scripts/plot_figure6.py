# Python imports
import os
import json

# 3rd party impoorts
import numpy as np
import cartopy.crs as ccrs

import matplotlib.pyplot as plt

# pycsep imports
from csep import load_catalog_forecast, load_json
from csep.models import Event, Polygon
from csep.core.regions import (
    magnitude_bins,
    create_space_magnitude_region,
    california_relm_region,
    masked_region
)
from csep.core.catalogs import CSEPCatalog
from csep.core.catalog_evaluations import spatial_test, number_test
from csep.utils.constants import SECONDS_PER_WEEK
from csep.utils.plots import plot_number_test, plot_spatial_test, plot_catalog
from csep.utils.scaling_relationships import WellsAndCoppersmith
from csep.utils.time_utils import epoch_time_to_utc_datetime, datetime_to_utc_epoch


def sort_by_longitude(coords):
    return coords[coords[:,0].argsort()]


def main():

    # file-path for results
    simulation_dir = f'../forecasts'
    results_dir = f'../data/'
    ucerf3_raw_data = os.path.join(simulation_dir, 'results_complete.bin.gz')
    m71_event = os.path.join(simulation_dir, 'm71_event.json')
    ucerf3_config = os.path.join(simulation_dir, 'config.json')
    catalog_fname = os.path.join(results_dir, 'evaluation_catalog.json')

    # magnitude range
    min_mw = 2.5
    max_mw = 8.95
    dmw = 0.1

    # define start and end epoch of the forecast
    with open(ucerf3_config, 'r') as config_file:
        config = json.load(config_file)
    start_epoch = config['startTimeMillis']
    end_epoch = start_epoch + SECONDS_PER_WEEK * 1000

    # number of fault radii to use for spatial filtering
    num_radii = 3

    # load evaluation catalog
    catalog = load_json(CSEPCatalog(), catalog_fname)

    # load event
    event = load_json(Event(), m71_event)
    event_epoch = datetime_to_utc_epoch(event.time)

    # define region and magnitude space
    rupture_length = WellsAndCoppersmith.mag_length_strike_slip(event.magnitude) * 1000
    aftershock_polygon = Polygon.from_great_circle_radius((event.longitude, event.latitude), num_radii*rupture_length, num_points=100)
    aftershock_region = masked_region(california_relm_region(dh_scale=4, use_midpoint=False), aftershock_polygon)

    mw_bins = magnitude_bins(min_mw, max_mw, dmw)
    smr = create_space_magnitude_region(aftershock_region, mw_bins)

    # create forecast object
    filters = [
        f'origin_time >= {start_epoch}',
        f'origin_time < {end_epoch}',
        f'magnitude >= {min_mw}'
    ]

    print('After filtering observation catalog')
    catalog = catalog.filter(filters).filter_spatial(region=smr)
    catalog = catalog.apply_mct(event.magnitude, event_epoch)
    print(catalog)

    u3etas_forecast = load_catalog_forecast(
        ucerf3_raw_data,
        start_time = epoch_time_to_utc_datetime(start_epoch),
        end_time = epoch_time_to_utc_datetime(end_epoch),
        region=smr,
        type='ucerf3',
        event=event,
        filters=filters,
        filter_spatial=True,
        apply_mct=True,
        apply_filters=True,
        store=False
    )

    # evaluate forecasting model
    print('computing spatial test results')
    s_test = spatial_test(u3etas_forecast, catalog)

    print('computing number test results')
    n_test = number_test(u3etas_forecast, catalog)

    # plot the results
    ax = plot_number_test(
        n_test,
        show=False,
        plot_args={
            'title': '',
            'xlabel_fontsize': 14,
            'ylabel_fontsize': 14
        })
    ax.get_figure().savefig('../figures/figure6b.png', dpi=300)
    ax = plot_spatial_test(s_test,
        show=False,
        plot_args={
            'title': '',
            'xlabel_fontsize': 14,
            'ylabel_fontsize': 14
        })
    ax.get_figure().savefig('../figures/figure6c.png', dpi=300)

    # plot forecast
    plot_args = {
        'projection': ccrs.Mercator(),
        'legend': True,
        'legend_loc': 1,
        'grid_fontsize': 16,
        'cmap': 'viridis',
        'grid_labels': True,
        'frameon': True,
        'mag_ticks': [2.5, 3.0, 3.5, 4.0],
        'markercolor': 'red',
        'clabel_fontsize': 16,
        'title': '',
        'legend_titlesize': 16,
        'legend_fontsize': 14,
        'mag_scale': 5
    }
    ax = u3etas_forecast.plot(plot_args=plot_args)
    ax = plot_catalog(catalog, plot_args=plot_args, ax=ax)
    ax.get_figure().savefig('../figures/figure6a.png', dpi=300)

    # saving evaluation results
    with open(f'../results/u3etas_{s_test.name}.json'.replace(" ","_").lower(), 'w') as wf:
        json.dump(s_test.to_dict(), wf, indent=4, separators=(',', ': '), sort_keys=True, default=str)

    with open(f'../results/u3etas_{n_test.name}.json'.replace(" ","_").lower(), 'w') as wf:
        json.dump(n_test.to_dict(), wf, indent=4, separators=(',', ': '), sort_keys=True, default=str)


if __name__ == "__main__":
    main()
