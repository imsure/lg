from timezonefinder import TimezoneFinder
import requests

import secrets
import constants as const


def unique_place_id():
    place_id = 1
    while True:
        yield place_id
        place_id += 1


def gps2timezone(lat, lon):
    tf = TimezoneFinder()
    tz = tf.timezone_at(lng=lon, lat=lat)
    return tz


def otp_date_time(now_pst, time):
    fields = time.split(':')
    hour = int(fields[0])
    minute = int(fields[1])

    suffix = 'am'
    if hour > 12:
        hour -= 12
        suffix = 'pm'
    elif hour == 12:
        suffix = 'pm'

    otp_time = '{}:{}{}'.format(hour, str(minute).zfill(2), suffix)
    otp_date = now_pst.strftime('%m-%d-%y')

    return otp_date, otp_time


def minutes2slot_id(minutes):
    """
    Convert time of day in total # of minutes to one of 96 time slot ID

    :param minutes: time of day in total # of minutes
    :return: slot id within [1, 96]
    """
    if minutes >= 1440:  # 24 * 60 = 1440
        minutes -= 1440
    return minutes // 15 + 1


def otp_walk_bike_time(from_lat, from_lon, to_lat, to_lon, tz):
    router = const.TIMEZONE2OTP_ROUTER[tz]
    url = "{}/otp/routers/{}/plan".format(secrets.OTP_URL, router)

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


if __name__ == '__main__':
    print(gps2timezone(39.75907, -104.99724))  # denver: America/Denver
    print(gps2timezone(30.2859758, -97.7404588))  # autsin: America/Chicago
    print(gps2timezone(29.7180255, -95.4002109))  # houston: America/Chicago
    print(gps2timezone(31.76000, -106.49157))  # elpaso: America/Denver
    print(gps2timezone(32.2315175, -110.9565735))  # tucson: America/Phoenix

    print(otp_date_time('15:30'))
