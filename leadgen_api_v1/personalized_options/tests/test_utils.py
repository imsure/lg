import unittest
import requests
from timezonefinder import TimezoneFinder

from .. import utils
from ..config import OTP_URL
from .. import constants as const

from . import fixture


class TestUtilsMethods(unittest.TestCase):
    tf = TimezoneFinder()

    def test_timezone_finder(self):
        tz = self.tf.timezone_at(lng=fixture.to_lon_tucson, lat=fixture.to_lat_tucson)
        self.assertEqual(const.TZ_MAP[tz], const.America_Phoenix)

        tz = self.tf.timezone_at(lng=fixture.to_lon_austin, lat=fixture.to_lat_austin)
        self.assertEqual(const.TZ_MAP[tz], const.America_Chicago)

        tz = self.tf.timezone_at(lng=fixture.to_lon_elpaso, lat=fixture.to_lat_elpaso)
        self.assertEqual(const.TZ_MAP[tz], const.America_Denver)

    def test_otp_router(self):
        tz = self.tf.timezone_at(lng=fixture.to_lon_tucson, lat=fixture.to_lat_tucson)
        router = const.TZ_OTP_ROUTER_MAP[const.TZ_MAP[tz]]
        self.assertEqual(router, 'tucson')

        tz = self.tf.timezone_at(lng=fixture.to_lon_austin, lat=fixture.to_lat_austin)
        router = const.TZ_OTP_ROUTER_MAP[const.TZ_MAP[tz]]
        self.assertEqual(router, 'austin')

        tz = self.tf.timezone_at(lng=fixture.to_lon_elpaso, lat=fixture.to_lat_elpaso)
        router = const.TZ_OTP_ROUTER_MAP[const.TZ_MAP[tz]]
        self.assertEqual(router, 'elpaso')

    def test_otp_walk_bike_tucson(self):
        url = "{}/otp/routers/{}/plan".format(OTP_URL, 'tucson')
        params = {
            'fromPlace': '{},{}'.format(fixture.from_lat_tucson, fixture.from_lon_tucson),
            'toPlace': '{},{}'.format(fixture.to_lat_tucson, fixture.to_lon_tucson),
            'mode': 'WALK',
            'arriveBy': 'false',
            'wheelchair': 'false',
            'locale': 'en',
        }
        r = requests.get(url, params=params)
        self.assertEqual(r.ok, True)
        self.assertEqual(r.status_code, 200)
        decoded = r.json()
        self.assertTrue('plan' in decoded)  # OTP should always return a travel plan for walk and bike
        # OTP should return exactly one itinerary for walk and bike travel plan
        self.assertTrue('itineraries' in decoded['plan'] and len(decoded['plan']['itineraries']) == 1)
        walk_time = decoded['plan']['itineraries'][0]['duration']

        params['mode'] = 'BICYCLE'
        r = requests.get(url, params=params)
        self.assertEqual(r.ok, True)
        self.assertEqual(r.status_code, 200)
        decoded = r.json()
        self.assertTrue('plan' in decoded)  # OTP should always return a travel plan for walk and bike
        # OTP should return exactly one itinerary for walk and bike travel plan
        self.assertTrue('itineraries' in decoded['plan'] and len(decoded['plan']['itineraries']) == 1)
        bike_time = decoded['plan']['itineraries'][0]['duration']

        t1, t2 = utils.otp_walk_bike_time(fixture.from_lat_tucson, fixture.from_lon_tucson,
                                          fixture.to_lat_tucson, fixture.to_lon_tucson,
                                          const.America_Phoenix)
        self.assertEqual(walk_time, t1)
        self.assertEqual(bike_time, t2)
        self.assertTrue(t1 > t2)  # walk time should be greater than bike time

    def test_otp_walk_bike_austin(self):
        url = "{}/otp/routers/{}/plan".format(OTP_URL, 'austin')
        params = {
            'fromPlace': '{},{}'.format(fixture.from_lat_austin, fixture.from_lon_austin),
            'toPlace': '{},{}'.format(fixture.to_lat_austin, fixture.to_lon_austin),
            'mode': 'WALK',
            'arriveBy': 'false',
            'wheelchair': 'false',
            'locale': 'en',
        }
        r = requests.get(url, params=params)
        self.assertEqual(r.ok, True)
        self.assertEqual(r.status_code, 200)
        decoded = r.json()
        self.assertTrue('plan' in decoded)  # OTP should always return a travel plan for walk and bike
        # OTP should return exactly one itinerary for walk and bike travel plan
        self.assertTrue('itineraries' in decoded['plan'] and len(decoded['plan']['itineraries']) == 1)
        walk_time = decoded['plan']['itineraries'][0]['duration']

        params['mode'] = 'BICYCLE'
        r = requests.get(url, params=params)
        self.assertEqual(r.ok, True)
        self.assertEqual(r.status_code, 200)
        decoded = r.json()
        self.assertTrue('plan' in decoded)  # OTP should always return a travel plan for walk and bike
        # OTP should return exactly one itinerary for walk and bike travel plan
        self.assertTrue('itineraries' in decoded['plan'] and len(decoded['plan']['itineraries']) == 1)
        bike_time = decoded['plan']['itineraries'][0]['duration']

        t1, t2 = utils.otp_walk_bike_time(fixture.from_lat_austin, fixture.from_lon_austin,
                                          fixture.to_lat_austin, fixture.to_lon_austin,
                                          const.America_Chicago)
        self.assertEqual(walk_time, t1)
        self.assertEqual(bike_time, t2)
        self.assertTrue(t1 > t2)  # walk time should be greater than bike time

    def test_otp_walk_bike_elpaso(self):
        url = "{}/otp/routers/{}/plan".format(OTP_URL, 'elpaso')
        params = {
            'fromPlace': '{},{}'.format(fixture.from_lat_elpaso, fixture.from_lon_elpaso),
            'toPlace': '{},{}'.format(fixture.to_lat_elpaso, fixture.to_lon_elpaso),
            'mode': 'WALK',
            'arriveBy': 'false',
            'wheelchair': 'false',
            'locale': 'en',
        }
        r = requests.get(url, params=params)
        self.assertEqual(r.ok, True)
        self.assertEqual(r.status_code, 200)
        decoded = r.json()
        self.assertTrue('plan' in decoded)  # OTP should always return a travel plan for walk and bike
        # OTP should return exactly one itinerary for walk and bike travel plan
        self.assertTrue('itineraries' in decoded['plan'] and len(decoded['plan']['itineraries']) == 1)
        walk_time = decoded['plan']['itineraries'][0]['duration']

        params['mode'] = 'BICYCLE'
        r = requests.get(url, params=params)
        self.assertEqual(r.ok, True)
        self.assertEqual(r.status_code, 200)
        decoded = r.json()
        self.assertTrue('plan' in decoded)  # OTP should always return a travel plan for walk and bike
        # OTP should return exactly one itinerary for walk and bike travel plan
        self.assertTrue('itineraries' in decoded['plan'] and len(decoded['plan']['itineraries']) == 1)
        bike_time = decoded['plan']['itineraries'][0]['duration']

        t1, t2 = utils.otp_walk_bike_time(fixture.from_lat_elpaso, fixture.from_lon_elpaso,
                                          fixture.to_lat_elpaso, fixture.to_lon_elpaso,
                                          const.America_Denver)
        self.assertEqual(walk_time, t1)
        self.assertEqual(bike_time, t2)
        self.assertTrue(t1 > t2)  # walk time should be greater than bike time
