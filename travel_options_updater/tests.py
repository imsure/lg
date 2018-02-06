import unittest
import constants as const
import utils
import fixture
import secrets
import requests
from timezonefinder import TimezoneFinder


class TestConstants(unittest.TestCase):

    def test_slot2time(self):
        self.assertEqual(const.SLOT2TIME[1], '00:00')
        self.assertEqual(const.SLOT2TIME[96], '23:45')
        self.assertEqual(const.SLOT2TIME[10], '02:15')

        with self.assertRaises(KeyError):
            const.SLOT2TIME[0]

        with self.assertRaises(KeyError):
            const.SLOT2TIME[97]

    def test_time2slot(self):
        self.assertEqual(const.TIME2SLOT['00:00'], 1)
        self.assertEqual(const.TIME2SLOT['00:15'], 2)
        self.assertEqual(const.TIME2SLOT['23:45'], 96)
        self.assertEqual(const.TIME2SLOT['23:30'], 95)

        with self.assertRaises(KeyError):
            const.TIME2SLOT['0:00']

        with self.assertRaises(KeyError):
            const.TIME2SLOT['24:00']

    def test_minutes2slot_id(self):
        self.assertEqual(utils.minutes2slot_id(0), 1)
        self.assertEqual(utils.minutes2slot_id(10), 1)
        self.assertEqual(utils.minutes2slot_id(15), 2)
        self.assertEqual(utils.minutes2slot_id(1440), 1)
        self.assertEqual(utils.minutes2slot_id(1439), 96)
        self.assertEqual(utils.minutes2slot_id(30), 3)
        self.assertEqual(utils.minutes2slot_id(31), 3)
        self.assertEqual(utils.minutes2slot_id(44), 3)


class TestUtilsMethods(unittest.TestCase):
    tf = TimezoneFinder()

    def test_timezone_finder(self):
        tz = self.tf.timezone_at(lng=fixture.to_lon_tucson, lat=fixture.to_lat_tucson)
        self.assertEqual(tz, const.TIMEZONE_DICT[const.America_Phoenix])

        tz = self.tf.timezone_at(lng=fixture.to_lon_austin, lat=fixture.to_lat_austin)
        self.assertEqual(tz, const.TIMEZONE_DICT[const.America_Chicago])

        tz = self.tf.timezone_at(lng=fixture.to_lon_elpaso, lat=fixture.to_lat_elpaso)
        self.assertEqual(tz, const.TIMEZONE_DICT[const.America_Denver])

    def test_otp_router(self):
        TZ_MAP = {
            'America/Phoenix': const.America_Phoenix,
            'America/Chicago': const.America_Chicago,
            'America/Denver': const.America_Denver,
        }
        tz = self.tf.timezone_at(lng=fixture.to_lon_tucson, lat=fixture.to_lat_tucson)
        router = const.TIMEZONE2OTP_ROUTER[TZ_MAP[tz]]
        self.assertEqual(router, 'tucson')

        tz = self.tf.timezone_at(lng=fixture.to_lon_austin, lat=fixture.to_lat_austin)
        router = const.TIMEZONE2OTP_ROUTER[TZ_MAP[tz]]
        self.assertEqual(router, 'austin')

        tz = self.tf.timezone_at(lng=fixture.to_lon_elpaso, lat=fixture.to_lat_elpaso)
        router = const.TIMEZONE2OTP_ROUTER[TZ_MAP[tz]]
        self.assertEqual(router, 'elpaso')

    def test_otp_walk_bike_tucson(self):
        url = "{}/otp/routers/{}/plan".format(secrets.OTP_URL, 'tucson')
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
        url = "{}/otp/routers/{}/plan".format(secrets.OTP_URL, 'austin')
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
        url = "{}/otp/routers/{}/plan".format(secrets.OTP_URL, 'elpaso')
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


if __name__ == '__main__':
    unittest.main()
