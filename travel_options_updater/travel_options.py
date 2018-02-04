import requests
import secrets

import utils
import constants as const


class TravelOption(object):

    otp_modes = ('TRANSIT,WALK', 'WALK', 'BICYCLE')

    def __init__(self, from_lat, from_lon, to_lat, to_lon, tz, time=None):
        self.parade_url = utils.timezone2parade_url(tz)
        self.otp_router = utils.timezone2otp_router(tz)
        self.from_lat = from_lat
        self.from_lon = from_lon
        self.to_lat = to_lat
        self.to_lon = to_lon
        self.time = time

    def parade(self):
        params = {
            'start_lat': self.from_lat,
            'start_lon': self.from_lon,
            'end_lat': self.to_lat,
            'end_lon': self.to_lon,
            'departure_time': self.time
        }
        r = requests.post(self.parade_url, json=params)
        json_decoded = r.json()
        if r.ok and json_decoded['status'] == 'success':
            return json_decoded['data']['estimated_travel_time']
        elif r.ok and json_decoded['status'] == 'fail':
            # TODO: log the corresponding message
            return None
        else:
            # TODO: log the corresponding message
            return None

    def otp(self):
        date, time = utils.otp_date_time(self.time)
        params = {
            'fromPlace': '{},{}'.format(self.from_lat, self.from_lon),
            'toPlace': '{},{}'.format(self.to_lat, self.to_lon),
            'time': time,
            'date': date,
            'mode': 'TRANSIT,WALK',
            'maxWalkDistance': const.MAX_WALK_DISTANCE,
            'arriveBy': 'false',
            'wheelchair': 'false',
            'locale': 'en',
        }
        url = "{}/otp/routers/{}/plan".format(secrets.OTP_URL, self.otp_router)
        r = requests.get(url, params=params)
        decoded = r.json()
        if r.ok and 'plan' in decoded and 'itineraries' in decoded['plan']:
            iti = decoded['plan']['itineraries'][0]  # first itinerary is the best option
                # print(iti['duration'], iti['walkTime'], iti['waitingTime'], iti['fare']['fare']['regular']['cents'])
            walk_time_ingress = 0
            walk_time_egress = 0
            legs = iti['legs']
            for leg in legs:
                if leg['mode'] == 'WALK' and leg['from']['name'] == 'Origin':
                    walk_time_ingress = leg['duration']
                if leg['mode'] == 'WALK' and leg['to']['name'] == 'Destination':
                    walk_time_egress = leg['duration']

            print(iti['duration'], iti['walkTime'], iti['waitingTime'], iti['fare']['fare']['regular']['cents'], walk_time_ingress, walk_time_egress)

        # print(r.text)
        print(r.status_code)


if __name__ == '__main__':
    # option = TravelOption(32.23114, -110.94548, 32.2866043, -110.9473657, '17:15')
    option = TravelOption(30.2859758, -97.7404588, 30.2727757, -97.7522587, 'America/Chicago', '09:15')
    tt_parade = option.parade()
    print(tt_parade)
    option.otp()
    # parade()
