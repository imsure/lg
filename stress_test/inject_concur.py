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
    activities = []

    # Generate activities for each city
    for city in config.ROUTER_NAMES:
        router = common.OtpRouter(city)
        for i in range(0, config.ACTIVITY_NUM_PER_CITY):
            activities.append(common.make_activity(router))

    # max workers set to 10, default is 2
    session = FuturesSession(max_workers=10)
    # headers = {'Authorization': 'Token {}'.format(config.AUTH_TOKEN)}
    session.headers['Authorization'] = 'Token {}'.format(config.AUTH_TOKEN)
    futures = []
    for activity in activities:
        start = datetime.now()
        from_id = next(place_id_iter)
        to_id = next(place_id_iter)
        url = config.LEADGEN_URL + 'activity/{}/{}/'.format(from_id, to_id)
        f = session.put(url, json=activity, background_callback=bg_cb)
        futures.append((f, start))

    # wait for requests to complete
    index = 1
    for f in futures:
        res = f[0].result()
        start = f[1]
        delta = res.end - start
        print(index, res.status_code, delta.microseconds/1e3)
        index += 1
