import glob
import math
import random
import zipfile
import pandas as pd

import config


WEEKDAY = 'WD'
WEEKEND = 'WN'
MONDAY = 'MO'
TUESDAY = 'TU'
WEDNESDAY = 'WE'
THURSDAY = 'TH'
FRIDAY = 'FR'
SATURDAY = 'SA'
SUNDAY = 'SU'

DAY_OF_WEEK_VALID_SET = {MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY, WEEKDAY, WEEKEND}
DAY_OF_WEEK_VALID_SET1 = {MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY}
DAY_OF_WEEK_VALID_SET2 = {MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, WEEKEND}
DAY_OF_WEEK_VALID_SET3 = {WEEKDAY, SATURDAY, SUNDAY}
DAY_OF_WEEK_VALID_SET4 = {WEEKDAY, WEEKEND}

Day_of_Week_Options = (
    DAY_OF_WEEK_VALID_SET1, DAY_OF_WEEK_VALID_SET2,
    DAY_OF_WEEK_VALID_SET3, DAY_OF_WEEK_VALID_SET4,
)


class OtpRouter(object):
    def __init__(self, name):
        self.name = name
        self.stops = extract_stops(name)

    def stop_lat_lon(self, index):
        return self.stops['stop_lat'][index], self.stops['stop_lon'][index]


def extract_stops(router_name):
    fname = glob.glob('{}/{}.*.zip'.format(config.GTFS_PATH, router_name))[0]
    f = zipfile.ZipFile(fname, 'r')
    df = pd.read_csv(f.open('stops.txt'))
    return df[['stop_lat', 'stop_lon']]


# https://gis.stackexchange.com/questions/25877/generating-random-locations-nearby
def random_geo_point(lat, lon, radius):
    r = radius/111300  # convert unit from meter to degree
    u = float(random.uniform(0.0, 1.0))
    v = float(random.uniform(0.0, 1.0))

    w = r * math.sqrt(u)
    t = 2 * math.pi * v
    x = w * math.cos(t)
    y = w * math.sin(t)

    return lat + x, lon + y


def random_prob_list():
    slot_id = random.randint(0, 93)

    # probability value does not matter as long as >= 25.0
    prob_list = [0.0] * 96
    prob_list[slot_id] = 33.333
    prob_list[slot_id+1] = 33.333
    prob_list[slot_id+2] = 33.333

    return prob_list


def make_activity(router):
    radius = 500  # meters
    indexes = random.sample(range(0, len(router.stops) - 1), 2)
    # Pick up from and to locations around randomly selected public transit stops
    from_lat, from_lon = router.stop_lat_lon(indexes[0])
    from_lat, from_lon = random_geo_point(from_lat, from_lon, radius)
    to_lat, to_lon = router.stop_lat_lon(indexes[1])
    to_lat, to_lon = random_geo_point(to_lat, to_lon, radius)

    patterns = {}
    day_of_week_option = Day_of_Week_Options[random.randint(0, 3)]
    for day_of_week in day_of_week_option:
        patterns[day_of_week] = random_prob_list()

    activity = {
        'from_lat': from_lat,
        'from_lon': from_lon,
        'to_lat': to_lat,
        'to_lon': to_lon,
        'purpose': 'W',  # trip purpose is irrelevant for testing, so just give a fixed value
        'patterns': patterns,
    }

    return activity
