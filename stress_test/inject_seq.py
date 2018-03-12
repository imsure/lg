"""
Injecting a large number of activities via LeadGen API and record response time
to see how LeadGen performs under stress.
"""

import requests

import config
import common


def unique_place_id():
    place_id = 337
    while True:
        yield place_id
        place_id += 1


if __name__ == '__main__':
    place_id_iter = unique_place_id()
    activities = []

    headers = {'Authorization': 'Token {}'.format(config.AUTH_TOKEN)}

    # Generate activities for each city
    for city in config.ROUTER_NAMES:
        router = common.OtpRouter(city)
        for i in range(0, config.ACTIVITY_NUM_PER_CITY):
            from_id = next(place_id_iter)
            to_id = next(place_id_iter)
            url = config.LEADGEN_URL + 'activity/{}/{}/'.format(from_id, to_id)
            activity = common.make_activity(router)
            r = requests.put(url, json=activity, headers=headers)
            print(r.status_code)
