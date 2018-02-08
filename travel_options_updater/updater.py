"""
Celery periodic tasks for updating travel options.
"""

import pytz
from datetime import datetime
import requests

from celery import Celery
from celery.schedules import crontab

import constants as const
import utils
import secrets
from travel_option_proxy import TravelOptionProxy

app = Celery('updater', broker='pyamqp://guest@localhost//')
app.conf.beat_schedule = {
    'task-daily-midnight-PST': {  # schedule to run at everyday midnight Pacific Standard Time
        'task': 'updater.parade_otp_updater',
        'schedule': crontab(minute=5, hour=8),  # UTC is 8 hours ahead of PST
        # 'schedule': crontab(minute='*/1'),  # for testing purpose
    },
    'task-every-15-minute': {  # schedule to run every 15-minute to update Uber options in real time
        'task': 'updater.uber_updater',
        'schedule': crontab(minute='*/15'),
        # 'schedule': crontab(minute='*/1'),  # for testing purpose
    },
}
app.conf.timezone = 'UTC'


def activity_detail(activity_id):
    headers = {'Authorization': 'Token {}'.format(secrets.API_TOKEN_ALI)}
    r = requests.get(secrets.LEADGEN_URL + 'activity/{}/'.format(activity_id), headers=headers)
    if r.status_code == 200:
        return r.json()
    return None


@app.task
def parade_otp_updater():
    """
    Called everyday at Pacific time (PST) midnight 00:00 to
    update travel options provided by Parade and OTP.

    Updating logic:
    1. Get the current date and day_of_week in PST.
    2. API call to LeadGen to get a list of travel options matching the day_of_week:
       GET travel_options/day_of_week/
       Response: [{'id': travel_option_pk, 'activity': activity_id, 'slot_id': slot_id, 'tz': timezone}]
    3. Bring in the activity object:
       GET activity/activity_id/
       Update walk_time and bike_time for the activity if they are none
    4. For each travel option, update travel plans accordingly:
       4-1 query Parade & OTP to get available plans, construct the request body
       4-2 PUT travel_options/travel_option_pk/
    """
    now_pst = datetime.now(pytz.timezone('US/Pacific'))
    day_of_week_exact = const.DAY_OF_WEEK_MAP[now_pst.weekday()]
    if now_pst.weekday() <= 4:
        day_of_week_general = const.WEEKDAY
    else:
        day_of_week_general = const.WEEKEND

    headers = {'Authorization': 'Token {}'.format(secrets.API_TOKEN_ALI)}
    r1 = requests.get(secrets.LEADGEN_URL + 'travel_options/{}/'.format(day_of_week_exact), headers=headers)
    r2 = requests.get(secrets.LEADGEN_URL + 'travel_options/{}/'.format(day_of_week_general), headers=headers)

    activity_dict = {}
    travel_options = r1.json() + r2.json()
    for option in travel_options:
        activity_id = option['activity']
        if activity_id not in activity_dict:
            activity_dict[activity_id] = activity_detail(activity_id)
        activity = activity_dict[activity_id]
        proxy = TravelOptionProxy(from_lat=activity['from_lat'], from_lon=activity['from_lon'],
                                  to_lat=activity['to_lat'], to_lon=activity['to_lon'],
                                  timezone=option['tz'], date=now_pst,
                                  time=const.SLOT2TIME[option['slot_id']])

        if activity['walk_time'] is None or activity['walk_time'] is None:
            walk_time = proxy.otp_walk_bike(mode='WALK')
            bike_time = proxy.otp_walk_bike(mode='BICYCLE')
            r = requests.put(secrets.LEADGEN_URL + 'activity/{}/{}/{}/'.format(activity_id, walk_time, bike_time),
                             headers=headers)
            if r.status_code == 200:
                print('Updated walk_time & bike_time for activity {}.'.format(activity_id))
                activity['walk_time'] = walk_time
                activity['bike_time'] = bike_time

        modes = {}

        drive_option = proxy.parade()
        if drive_option is not None:
            modes['drive'] = drive_option

        transit_option = proxy.otp_transit()
        if transit_option is not None:
            modes['transit'] = transit_option

        if modes:  # empty dict {} evaluate to be False
            r = requests.put(secrets.LEADGEN_URL + 'travel_options/{}/'.format(option['id']),
                             json=modes, headers=headers)
            if r.ok and r.status_code == 200:
                print('Updated driving & transit fields for option {}.'.format(option['id']))
            if not r.ok:
                pass  # TODO: log the message


@app.task
def uber_updater():
    """
    Called every 15 minutes to update travel options provided by UberX and UberPool.

    Updating logic:
    1. Convert current UTC time to Tucson, Austin and El Paso local times.
    2. Convert local time to the corresponding day_of_week and slot_id.
    3. API call to LeadGen to bring in corresponding travel options:
       GET travel_options/<day_of_week>/<slot_id>/<tz>/
    4. For each travel option, query Uber API to get uber estimates and
       update this information via LeadGen API:
       PUT travel_options/travel_option_pk/
    """
    fmt = "%Y-%m-%d %H:%M:%S %Z%z"
    now_utc = datetime.now(pytz.timezone('UTC'))
    for tz, tz_name in const.TIMEZONE_DICT.items():
        now_local = now_utc.astimezone(pytz.timezone(tz_name))
        slot_id = utils.minutes2slot_id(now_local.hour * 60 + now_local.minute)
        day_of_week_exact = const.DAY_OF_WEEK_MAP[now_local.weekday()]
        print('Local Time at {}: {}, {} (slot: {})'.format(tz_name, day_of_week_exact,
                                                           now_local.strftime(fmt), slot_id))
        if now_local.weekday() <= 4:
            day_of_week_general = const.WEEKDAY
        else:
            day_of_week_general = const.WEEKEND

        headers = {'Authorization': 'Token {}'.format(secrets.API_TOKEN_ALI)}
        r1 = requests.get(secrets.LEADGEN_URL + 'travel_options/{}/{}/{}/'.
                          format(day_of_week_exact, slot_id, tz), headers=headers)
        r2 = requests.get(secrets.LEADGEN_URL + 'travel_options/{}/{}/{}/'.
                          format(day_of_week_general, slot_id, tz), headers=headers)

        travel_options = r1.json() + r2.json()
        # print('# of uber options to be updated: {}'.format(len(travel_options)))
        activity_dict = {}
        for option in travel_options:
            activity_id = option['activity']
            if activity_id not in activity_dict:
                activity_dict[activity_id] = activity_detail(activity_id)
            activity = activity_dict[activity_id]
            proxy = TravelOptionProxy(from_lat=activity['from_lat'], from_lon=activity['from_lon'],
                                      to_lat=activity['to_lat'], to_lon=activity['to_lon'],
                                      timezone=tz, date=now_local,
                                      time=const.SLOT2TIME[option['slot_id']])

            modes = {}
            uber_option = proxy.uber()
            if uber_option:  # empty dict {} evaluate to be False
                modes['uber'] = uber_option

            if modes:  # empty dict {} evaluate to be False
                r = requests.put(secrets.LEADGEN_URL + 'travel_options/{}/'.format(option['id']),
                                 json=modes, headers=headers)
                if r.ok and r.status_code == 200:
                    print('Updated uber field for option {}.'.format(option['id']))
                if not r.ok:
                    pass  # TODO: log the message
