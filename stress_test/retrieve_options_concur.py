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


# session callback
def bg_cb(sess, resp):
    # record the time the response was received
    resp.end = datetime.now()


def unique_place_id():
    place_id = 1
    while True:
        yield place_id
        place_id += 1


if __name__ == '__main__':
    place_id_iter = unique_place_id()
    reqs = []

    activity_num = 1
    for i in range(0, activity_num):
        from_id = next(place_id_iter)
        to_id = next(place_id_iter)
        for day_of_week in common.DAY_OF_WEEK_VALID_SET4:
            for slot_id in range(1, 97):
                reqs.append('{}personalized_options/{}/{}/{}/{}/'.format(config.LEADGEN_URL,
                                                                         from_id, to_id,
                                                                         day_of_week, slot_id))

    # max workers set to 10, default is 2
    session = FuturesSession(max_workers=10)
    # headers = {'Authorization': 'Token {}'.format(config.AUTH_TOKEN)}
    session.headers['Authorization'] = 'Token {}'.format(config.AUTH_TOKEN)
    futures = []
    for req in reqs:
        start = datetime.now()
        f = session.get(req, background_callback=bg_cb)
        futures.append((f, start))

    # wait for requests to complete
    index = 1
    for f in futures:
        res = f[0].result()
        start = f[1]
        delta = res.end - start
        print(index, res.status_code, delta.microseconds/1e3)
        index += 1
