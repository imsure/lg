import requests
from .constants import TZ_OTP_ROUTER_MAP
from .config import OTP_URL


def otp_walk_bike_time(from_lat, from_lon, to_lat, to_lon, tz):
    router = TZ_OTP_ROUTER_MAP[tz]
    url = "{}/otp/routers/{}/plan".format(OTP_URL, router)

    params = {
        'fromPlace': '{},{}'.format(from_lat, from_lon),
        'toPlace': '{},{}'.format(to_lat, to_lon),
        'mode': 'WALK',
        'arriveBy': 'false',
        'wheelchair': 'false',
        'locale': 'en',
    }

    r = requests.get(url, params=params)
    decoded = r.json()
    walk_time = None
    if r.ok and 'plan' in decoded and 'itineraries' in decoded['plan']:
        iti = decoded['plan']['itineraries'][0]
        walk_time = iti['duration']

    params['mode'] = 'BICYCLE'
    r = requests.get(url, params=params)
    decoded = r.json()
    bike_time = None
    if r.ok and 'plan' in decoded and 'itineraries' in decoded['plan']:
        iti = decoded['plan']['itineraries'][0]
        bike_time = iti['duration']

    return walk_time, bike_time
