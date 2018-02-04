import requests
from pprint import pprint

import utils
import constants as const
import secrets

# Default GPS points used for testing.
from_lat_tucson = 32.27908
from_lon_tucson = -110.94449
to_lat_tucson = 32.22997
to_lon_tucson = -110.95475

from_lat_austin = 30.2859758
from_lon_austin = -97.7404588
to_lat_austin = 30.2727757
to_lon_austin = -97.7522587

from_lat_elpaso = 31.76000
from_lon_elpaso = -106.49157
to_lat_elpaso = 31.75236
to_lon_elpaso = -106.47984


def slot_id_to_time_map():
    d = {}
    _d = {}
    for i in range(1, 97):
        t = (i - 1) * 15
        m = t // 60
        s = t % 60
        t_str = '{}:{}'.format(str(m).zfill(2), str(s).zfill(2))
        d[i] = t_str
        _d[t_str] = i
    pprint(d)
    pprint(_d)


def activity_tucson():
    prob_list1 = [0] * 96
    prob_list1[const.TIME2SLOT['08:00']-1] = 30
    prob_list1[const.TIME2SLOT['08:15']-1] = 40
    prob_list1[const.TIME2SLOT['08:30']-1] = 30

    prob_list2 = [0.0] * 96
    prob_list2[const.TIME2SLOT['18:00']-1] = 33.333
    prob_list2[const.TIME2SLOT['18:30']-1] = 33.333
    prob_list2[const.TIME2SLOT['19:00']-1] = 33.333

    patterns = {
        'MO': prob_list1,
        'WE': prob_list2,
    }

    activity = {
        'from_lat': from_lat_tucson,
        'from_lon': from_lon_tucson,
        'to_lat': to_lat_tucson,
        'to_lon': to_lon_tucson,
        'purpose': 'W',
        'patterns': patterns,
    }
    return activity


def activity_austin():
    probabilities = [0.0] * 96
    probabilities[const.TIME2SLOT['23:30']-1] = 50
    probabilities[const.TIME2SLOT['23:45']-1] = 50

    patterns = {
        'SA': probabilities,
    }

    activity = {
        "from_lat": from_lat_austin,
        "from_lon": from_lon_austin,
        "to_lat": to_lat_austin,
        "to_lon": to_lon_austin,
        "purpose": "H",  # home
        'patterns': patterns,
    }
    return activity


def activity_elpaso():
    probabilities = [0.0] * 96
    probabilities[const.TIME2SLOT['12:00']-1] = 50
    probabilities[const.TIME2SLOT['12:15']-1] = 25
    probabilities[const.TIME2SLOT['12:30']-1] = 25

    patterns = {
        'WD': probabilities,
    }

    activity = {
        "from_lat": from_lat_elpaso,
        "from_lon": from_lon_elpaso,
        "to_lat": to_lat_elpaso,
        "to_lon": to_lon_elpaso,
        "purpose": "W",  # work
        'patterns': patterns,
    }
    return activity


if __name__ == '__main__':
    place_id_iter = utils.unique_place_id()

    activity = activity_tucson()
    headers = {'Authorization': 'Token {}'.format(secrets.API_TOKEN_ALI)}
    from_id = next(place_id_iter)
    to_id = next(place_id_iter)
    r = requests.put(secrets.LEADGEN_URL + 'activity/{}/{}/'.format(from_id, to_id),
                     json=activity, headers=headers)
    print(r.status_code)
    print(r.text)

    r = requests.get(secrets.LEADGEN_URL + 'travel_options/MO/', headers=headers)
    print(r.text)
    print(r.status_code)

    r = requests.get(secrets.LEADGEN_URL + 'travel_options/WD/', headers=headers)
    print(r.text)
    print(r.status_code)

    r = requests.get(secrets.LEADGEN_URL + 'travel_options/WE/', headers=headers)
    print(r.text)
    print(r.status_code)

    activity = activity_austin()
    from_id = next(place_id_iter)
    to_id = next(place_id_iter)
    r = requests.put(secrets.LEADGEN_URL + 'activity/{}/{}/'.format(from_id, to_id),
                     json=activity, headers=headers)
    print(r.status_code)
    print(r.text)

    activity = activity_elpaso()
    from_id = next(place_id_iter)
    to_id = next(place_id_iter)
    r = requests.put(secrets.LEADGEN_URL + 'activity/{}/{}/'.format(from_id, to_id),
                     json=activity, headers=headers)
    print(r.status_code)
    print(r.text)

    # r = requests.get(secrets.LEADGEN_URL + 'travel_options/WE/76/AP/', headers=headers)
    # print(r.text)
    # print(r.status_code)
    #
    # option = {
    #     'drive': {'travel_time': 123.45, 'distance': 456.123},
    #     'transit': {'travel_time': 789, 'cost': 1.25, 'wait_time': 9}
    # }
    # r = requests.put(secrets.LEADGEN_URL + 'travel_options/5/', json=option, headers=headers)
    # print(r.text)
    # print(r.status_code)
    #
    # option = {
    #     'uber': {'travel_time': 135, 'wait_time': 246, 'cost': '$4-7'}
    # }
    # r = requests.put(secrets.LEADGEN_URL + 'travel_options/5/', json=option, headers=headers)
    # print(r.text)
    # print(r.status_code)
