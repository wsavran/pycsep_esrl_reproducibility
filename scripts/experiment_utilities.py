from datetime import datetime

import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

from csep import load_gridded_forecast, load_catalog
from csep.utils.time_utils import (
    strptime_to_utc_datetime,
    strptime_to_utc_epoch,
    datetime_to_utc_epoch
)

class EvaluationConfig:

    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.forecasts = {}
        self.evaluation_catalog = None
        self.catalog_loader = None
        self.seed = None
        self.t_test_benchmark = None


def load_california_catalog(filename):
    """ Loads catalog as presented by Table 1 in Zechar et al., 2013 """
    month_str_to_num = {
        'Jan': 1,
        'Feb': 2,
        'Mar': 3,
        'Apr': 4,
        'May': 5,
        'Jun': 6,
        'Jul': 7,
        'Aug': 8,
        'Sep': 9,
        'Oct': 10,
        'Nov': 11,
        'Dec': 12
    }
    eventlist = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            line = line.strip().split()
            # event_id
            event_id = line[0]
            # day of month
            day = line[1]
            # month
            month_str = line[2]
            month = month_str_to_num[month_str]
            # year
            year = line[3]
            # time string
            time = line[4]
            # create origin time
            time_string = "{0}-{1}-{2} {3}".format(year, month, day, time)
            origin_time = strptime_to_utc_epoch(time_string, format="%Y-%m-%d %H:%M")
            # latitude
            latitude = float(line[5])
            # longitude
            longitude = float(line[6])
            # magnitude
            magnitude = float(line[7])
            # depth
            depth = float(line[8])
            event_tuple = (
                event_id,
                origin_time,
                latitude,
                longitude,
                depth,
                magnitude
            )
            eventlist.append(event_tuple)
    return eventlist

def load_italian_catalog(fname):
    class ColumnIndex:
        Longitude = 0
        Latitude = 1
        DecimalYear = 2
        Month = 3
        Day = 4
        Hour = 5
        Minute = 6
        Second = 7
        Magnitude = 8
        Depth = 9
        
    def parse_datetime(line):
        year = int(line[ColumnIndex.DecimalYear])
        month = int(line[ColumnIndex.Month])
        day = int(line[ColumnIndex.Day])
        hour = int(line[ColumnIndex.Hour])
        minute = int(line[ColumnIndex.Minute])
        decimal_second = line[ColumnIndex.Second]
        seconds = int(np.floor(decimal_second))
        microseconds = int((decimal_second - seconds) * 1e6)
        dt = datetime(
            year,
            month,
            day,
            hour,
            minute,
            seconds,
            microseconds
        )
        return dt
    
    # arrange file into list of tuples
    out = []
    catalog_data = np.loadtxt(fname)
    for event_id, line in enumerate(catalog_data):
        event_tuple = ()
        event_tuple = (
            event_id,
            datetime_to_utc_epoch(parse_datetime(line)),
            line[ColumnIndex.Latitude],
            line[ColumnIndex.Longitude],
            line[ColumnIndex.Depth],
            line[ColumnIndex.Magnitude],
        )
        out.append(event_tuple)
    return out

# configuration for california testing regions 
california_experiment = EvaluationConfig()
california_experiment.start_time = strptime_to_utc_datetime('2006-01-01 00:00:00.0')
california_experiment.end_time = strptime_to_utc_datetime('2011-01-01 00:00:00.0')
california_experiment.evaluation_catalog = './data/evaluation_catalog_zechar2013_merge.txt'
california_experiment.catalog_loader = load_california_catalog
california_experiment.forecasts = {
    'helmstetter': './forecasts/helmstetter_et_al.hkj.aftershock-fromXML.dat',
    'bird_liu': './forecasts/bird_liu.neokinema-fromXML.dat',
    'ebel': './forecasts/ebel.aftershock.corrected-fromXML.dat'
}
california_experiment.seed = 123456
california_experiment.t_test_benchmark = 'helmstetter'

# configuration for italian testing region
italy_experiment = EvaluationConfig()
italy_experiment.start_time = strptime_to_utc_datetime('2010-01-01 00:00:00.0')
italy_experiment.end_time = strptime_to_utc_datetime('2015-01-01 00:00:00.0')
italy_experiment.evaluation_catalog = './data/SRL_2018031_esupp_Table_S1.txt'
italy_experiment.catalog_loader = load_italian_catalog
italy_experiment.forecasts = {
    'lombardi': './forecasts/lombardi.DBM.italy.5yr.2010-01-01.dat',
    'meletti': './forecasts/meletti.MPS04.italy.5yr.2010-01-01.dat',
    'werner-m1': './forecasts/werner.HiResSmoSeis-m1.italy.5yr.2010-01-01.dat'
}
italy_experiment.seed = 123456
italy_experiment.t_test_benchmark = 'meletti'

