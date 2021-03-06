"""
Celery periodic tasks for updating travel options.
"""

import pytz
from datetime import datetime
import requests
import logging

from celery import Celery
from celery.schedules import crontab
from celery.utils.log import get_task_logger

import constants as const
import utils
import secrets
from travel_option_proxy import TravelOptionProxy

app = Celery('uber_updater', broker='pyamqp://guest@localhost//')
app.conf.beat_schedule = {
    'task-every-15-minute': {  # schedule to run every 15-minute to update Uber options in real time
        'task': 'uber_updater.uber_updater',
        'schedule': crontab(minute='*/15'),
        # 'schedule': crontab(minute='*/1'),  # for testing purpose
    },
}
app.conf.timezone = 'UTC'

logger = get_task_logger(__name__)


def activity_detail(activity_id):
    headers = {'Authorization': 'Token {}'.format(secrets.API_TOKEN_ALI)}
    r = requests.get(secrets.LEADGEN_URL + 'activity/{}/'.format(activity_id), headers=headers)
    if r.status_code == 200:
        return r.json()
    return None


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
    query_count_uber = 0

    now_utc = datetime.now(pytz.timezone('UTC'))
    for tz, tz_name in const.TIMEZONE_DICT.items():
        now_local = now_utc.astimezone(pytz.timezone(tz_name))
        slot_id = utils.minutes2slot_id(now_local.hour * 60 + now_local.minute)
        day_of_week_exact = const.DAY_OF_WEEK_MAP[now_local.weekday()]
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
        activity_dict = {}
        query_count_uber += len(travel_options)
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
                if not r.ok:
                    pass  # TODO: log the message

    logger.info('# of queries made to Uber: {}'.format(query_count_uber))
