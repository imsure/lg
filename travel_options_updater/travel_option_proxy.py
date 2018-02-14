import requests
import secrets

import utils
import constants as const


class TravelOptionProxy(object):
    """
    Serves as a proxy for the `updater` to get travel options from multiple sources (Parade,
    OTP and Uber).
    """

    def __init__(self, from_lat, from_lon, to_lat, to_lon, timezone, date, time):
        self.from_lat = from_lat
        self.from_lon = from_lon
        self.to_lat = to_lat
        self.to_lon = to_lon
        self.timezone = timezone
        self.otp_date, self.otp_time = utils.otp_date_time(date, time)
        self.time = time
        self.parade_url = const.TIMEZONE2PARADE_ELB[self.timezone]
        self.otp_router = const.TIMEZONE2OTP_ROUTER[self.timezone]

    def __repr__(self):
        return str({
            'from_lat': self.from_lat,
            'from_lon': self.from_lon,
            'to_lat': self.to_lat,
            'to_lon': self.to_lon,
            'timezone': self.timezone,
            'otp_date': self.otp_date,
            'otp_time': self.otp_time,
            'time': self.time,
            'parade_url': self.parade_url,
            'otp_router': self.otp_router,
        })

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
            travel_time = json_decoded['data']['estimated_travel_time'] * 60  # minutes -> seconds
            travel_time = round(travel_time, 2)
            distance = json_decoded['data']['distance']
            distance = round(distance, 2)
            return {
                'travel_time': travel_time,
                'distance': distance,
            }
        elif r.ok and json_decoded['status'] == 'fail':
            # TODO: log the corresponding message
            return None
        else:
            # TODO: log the corresponding message
            return None

    def otp_transit(self):
        params = {
            'fromPlace': '{},{}'.format(self.from_lat, self.from_lon),
            'toPlace': '{},{}'.format(self.to_lat, self.to_lon),
            'time': self.otp_time,
            'date': self.otp_date,
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
            walk_time_ingress = 0
            walk_time_egress = 0
            legs = iti['legs']
            for leg in legs:
                if leg['mode'] == 'WALK' and leg['from']['name'] == 'Origin':
                    walk_time_ingress = leg['duration']
                if leg['mode'] == 'WALK' and leg['to']['name'] == 'Destination':
                    walk_time_egress = leg['duration']
            travel_time = iti['duration']
            wait_time = iti['waitingTime']
            if self.otp_router == 'tucson':
                cost = const.SUNTRAN_FARE
            else:
                try:
                    cost = iti['fare']['fare']['regular']['cents']
                    cost = cost / 100  # cents -> dollars
                except KeyError:
                    return None

            return {
                'travel_time': travel_time,
                'wait_time': wait_time,
                'cost': cost,
                'walk_time_ingress': walk_time_ingress,
                'walk_time_egress': walk_time_egress,
            }
        else:
            return None

    def otp_walk_bike(self, mode):
        params = {
            'fromPlace': '{},{}'.format(self.from_lat, self.from_lon),
            'toPlace': '{},{}'.format(self.to_lat, self.to_lon),
            'mode': mode,
            'arriveBy': 'false',
            'wheelchair': 'false',
            'locale': 'en',
        }
        url = "{}/otp/routers/{}/plan".format(secrets.OTP_URL, self.otp_router)
        r = requests.get(url, params=params)
        decoded = r.json()
        if r.ok and 'plan' in decoded and 'itineraries' in decoded['plan']:
            travel_time = decoded['plan']['itineraries'][0]['duration']
            return travel_time
        return None

    def uber_time_estimate(self, product_id):
        url = 'https://api.uber.com/v1.2/estimates/time'
        params = {
            'start_latitude': self.from_lat,
            'start_longitude': self.from_lon,
            'product_id': product_id,
        }
        headers = {
            'Content-Type': 'application/json',
            'Accept-Language': 'en_US',
            'Authorization': 'Token {}'.format(secrets.UBER_TOKEN)
        }

        r = requests.get(url, headers=headers, params=params)
        if r.ok and r.status_code == 200:
            decoded = r.json()
            if 'times' in decoded and len(decoded['times']) > 0:
                wait_time = decoded['times'][0]['estimate']
                return wait_time
            else:
                return None
        else:
            return None  # TODO: log the message

    def uber_price_estimate(self, product_id):
        url = 'https://api.uber.com/v1.2/estimates/price'
        params = {
            'start_latitude': self.from_lat,
            'start_longitude': self.from_lon,
            'end_latitude': self.to_lat,
            'end_longitude': self.to_lon,
        }
        headers = {
            'Content-Type': 'application/json',
            'Accept-Language': 'en_US',
            'Authorization': 'Token {}'.format(secrets.UBER_TOKEN)
        }

        r = requests.get(url, headers=headers, params=params)
        decoded = r.json()
        if r.ok and r.status_code == 200 and 'prices' in decoded:
            price_list = decoded['prices']
            for price in price_list:
                if price['product_id'] == product_id:
                    return price['duration'], price['estimate']
            return None, None  # no matching prodcut id found
        else:
            return None, None  # TODO: log the message

    def uber_product(self, product_name):
        product_detail = {}
        if product_name in const.UBER_Name2ID[self.otp_router]:
            product_id = const.UBER_Name2ID[self.otp_router][product_name]
            wait_time = self.uber_time_estimate(product_id)
            travel_time, cost = self.uber_price_estimate(product_id)
            if wait_time is not None and travel_time is not None and cost is not None:
                product_detail = {'travel_time': travel_time, 'wait_time': wait_time, 'cost': cost}
        return product_detail

    def uber(self):
        uberx = self.uber_product('uberx')
        uberpool = self.uber_product('uberpool')

        uber_option = {}
        if uberx:
            uber_option['uberx'] = uberx
        if uberpool:
            uber_option['uberpool'] = uberpool

        return uber_option
