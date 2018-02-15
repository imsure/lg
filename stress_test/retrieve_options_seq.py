"""
Injecting a large number of activities via LeadGen API and record response time
to see how LeadGen performs under stress.
"""

import requests
import json
import sys
from datetime import datetime
from requests_futures.sessions import FuturesSession  # Asynchronous HTTP Requests

import config
import common


def unique_place_id():
    place_id = 1
    while True:
        yield place_id
        place_id += 1


if __name__ == '__main__':
    place_id_iter = unique_place_id()

    headers = {'Authorization': 'Token {}'.format(config.AUTH_TOKEN)}
    activity_num = 2
    for i in range(0, activity_num):
        from_id = next(place_id_iter)
        to_id = next(place_id_iter)
        for day_of_week in common.DAY_OF_WEEK_VALID_SET:
            for slot_id in range(1, 97):
                start = datetime.now()
                r = requests.get('{}personalized_options/{}/{}/{}/{}/'.format(config.LEADGEN_URL,
                                                                              from_id, to_id,
                                                                              day_of_week, slot_id),
                                 headers=headers)
                end = datetime.now()
                print(r.status_code, (end-start).microseconds/1e3)
