import json

from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from ..models import Activity, TravelOption
from . import fixture
from .. import constants as const


place_id_iter = fixture.unique_place_id()


def activity_tucson():
    activity = {
        'from_lat': fixture.from_lat_tucson,
        'from_lon': fixture.from_lon_tucson,
        'to_lat': fixture.to_lat_tucson,
        'to_lon': fixture.to_lon_tucson,
        'purpose': const.WORK,
    }

    prob_list = [0] * 96
    prob_list[0] = 30
    prob_list[1] = 40
    prob_list[2] = 30
    patterns = {
        const.WEEKDAY: prob_list,
    }
    activity['patterns'] = patterns

    return activity


def activity_tucson_update():
    activity = {
        'from_lat': fixture.from_lat_tucson,
        'from_lon': fixture.from_lon_tucson,
        'to_lat': fixture.to_lat_tucson,
        'to_lon': fixture.to_lon_tucson,
        'purpose': const.WORK,
    }

    prob_list = [0] * 96
    prob_list[3] = 50
    prob_list[4] = 50
    patterns = {
        const.THURSDAY: prob_list,
    }
    activity['patterns'] = patterns

    return activity


def activity_austin():
    activity = {
        'from_lat': fixture.from_lat_austin,
        'from_lon': fixture.from_lon_austin,
        'to_lat': fixture.to_lat_austin,
        'to_lon': fixture.to_lon_austin,
        'purpose': const.HOME,
    }

    prob_list = [0.0] * 96
    prob_list[94] = 75
    prob_list[95] = 25.0
    patterns = {
        const.MONDAY: prob_list,
    }
    activity['patterns'] = patterns

    return activity


def activity_elpaso():
    activity = {
        'from_lat': fixture.from_lat_elpaso,
        'from_lon': fixture.from_lon_elpaso,
        'to_lat': fixture.to_lat_elpaso,
        'to_lon': fixture.to_lon_elpaso,
        'purpose': const.SCHOOL,
    }

    prob_list1 = [0.0] * 96
    prob_list1[93] = 5  # below the threshold
    prob_list1[94] = 70
    prob_list1[95] = 25.0

    prob_list2 = [0.0] * 96
    prob_list2[0] = 5  # below the threshold
    prob_list2[1] = 90
    prob_list2[2] = 5  # below the threshold
    patterns = {
        const.WEEKDAY: prob_list1,
        const.SATURDAY: prob_list2,
    }
    activity['patterns'] = patterns

    return activity


def activity_prob_list_more_than_96():
    activity = {
        'from_lat': fixture.from_lat_tucson,
        'from_lon': fixture.from_lon_tucson,
        'to_lat': fixture.to_lat_tucson,
        'to_lon': fixture.to_lon_tucson,
        'purpose': const.WORK,
    }

    prob_list = [0] * 97  # not allowed
    prob_list[0] = 30
    prob_list[1] = 40
    prob_list[2] = 30
    patterns = {
        const.WEEKDAY: prob_list,
    }
    activity['patterns'] = patterns

    return activity


def activity_prob_list_less_than_96():
    activity = {
        'from_lat': fixture.from_lat_tucson,
        'from_lon': fixture.from_lon_tucson,
        'to_lat': fixture.to_lat_tucson,
        'to_lon': fixture.to_lon_tucson,
        'purpose': const.WORK,
    }

    prob_list = [0] * 95  # not allowed
    prob_list[0] = 30
    prob_list[1] = 40
    prob_list[2] = 30
    patterns = {
        const.WEEKDAY: prob_list,
    }
    activity['patterns'] = patterns

    return activity


def activity_prob_total_above_100():
    activity = {
        'from_lat': fixture.from_lat_tucson,
        'from_lon': fixture.from_lon_tucson,
        'to_lat': fixture.to_lat_tucson,
        'to_lon': fixture.to_lon_tucson,
        'purpose': const.WORK,
    }

    prob_list = [0] * 96
    prob_list[0] = 30
    prob_list[1] = 40.11
    prob_list[2] = 30
    patterns = {
        const.WEEKDAY: prob_list,
    }
    activity['patterns'] = patterns

    return activity


def activity_prob_total_below_100():
    activity = {
        'from_lat': fixture.from_lat_tucson,
        'from_lon': fixture.from_lon_tucson,
        'to_lat': fixture.to_lat_tucson,
        'to_lon': fixture.to_lon_tucson,
        'purpose': const.WORK,
    }

    prob_list = [0] * 96
    prob_list[0] = 30
    prob_list[1] = 39.89
    prob_list[2] = 30
    patterns = {
        const.WEEKDAY: prob_list,
    }
    activity['patterns'] = patterns

    return activity


def activity_invalid_prob_value_type():
    activity = {
        'from_lat': fixture.from_lat_tucson,
        'from_lon': fixture.from_lon_tucson,
        'to_lat': fixture.to_lat_tucson,
        'to_lon': fixture.to_lon_tucson,
        'purpose': const.WORK,
    }

    prob_list = [0] * 96
    prob_list[0] = 30
    prob_list[1] = '40'  # not allowed
    prob_list[2] = 30
    patterns = {
        const.WEEKDAY: prob_list,
    }
    activity['patterns'] = patterns

    return activity


def activity_prob_value_below_zero():
    activity = {
        'from_lat': fixture.from_lat_tucson,
        'from_lon': fixture.from_lon_tucson,
        'to_lat': fixture.to_lat_tucson,
        'to_lon': fixture.to_lon_tucson,
        'purpose': const.WORK,
    }

    prob_list = [0] * 96
    prob_list[0] = 30
    prob_list[1] = -0.1  # not allowed
    prob_list[2] = 30
    patterns = {
        const.WEEKDAY: prob_list,
    }
    activity['patterns'] = patterns

    return activity


def activity_prob_value_above_100():
    activity = {
        'from_lat': fixture.from_lat_tucson,
        'from_lon': fixture.from_lon_tucson,
        'to_lat': fixture.to_lat_tucson,
        'to_lon': fixture.to_lon_tucson,
        'purpose': const.WORK,
    }

    prob_list = [0] * 96
    prob_list[0] = 30
    prob_list[1] = 100.1  # not allowed
    prob_list[2] = 30
    patterns = {
        const.WEEKDAY: prob_list,
    }
    activity['patterns'] = patterns

    return activity


class ActivityViewTest(APITestCase):

    def setUp(self):
        username = 'alex'
        email = 'alex@hacker.com'
        password = 'alex_knows_nothing'
        self.user = User.objects.create_user(username, email, password)

    def test_create_activity_tucson(self):
        """
        A valid activity in Tucson should be created and the corresponding
        travel option entries should be populated successfully.
        """
        from_id = next(place_id_iter)
        to_id = next(place_id_iter)
        activity = activity_tucson()

        client = APIClient()
        client.force_authenticate(user=self.user)
        r = client.put(reverse('create_update_activity', kwargs={'from_id': from_id, 'to_id': to_id}),
                       activity, format='json')
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

        activity_obj = Activity.objects.get(from_id=from_id, to_id=to_id)
        travel_options = TravelOption.objects.filter(activity_id=activity_obj.id, day_of_week=const.WEEKDAY)
        self.assertEqual(len(travel_options), 3)  # 3 entries should've been populated for this activity
        slots = [option.slot_id for option in travel_options]
        self.assertEqual(sorted(slots), [1, 2, 3])
        self.assertEqual([option.tz for option in travel_options], [const.America_Phoenix]*3)

    def test_create_activity_austin(self):
        """
        A valid activity in Austin should be created and the corresponding
        travel option entries should be populated successfully.
        """
        from_id = next(place_id_iter)
        to_id = next(place_id_iter)
        activity = activity_austin()

        client = APIClient()
        client.force_authenticate(user=self.user)
        r = client.put(reverse('create_update_activity', kwargs={'from_id': from_id, 'to_id': to_id}),
                       activity, format='json')
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

        activity_obj = Activity.objects.get(from_id=from_id, to_id=to_id)
        travel_options = TravelOption.objects.filter(activity_id=activity_obj.id, day_of_week=const.MONDAY)
        self.assertEqual(len(travel_options), 2)  # 2 entries should've been populated for this activity
        slots = [option.slot_id for option in travel_options]
        self.assertEqual(sorted(slots), [95, 96])
        self.assertEqual([option.tz for option in travel_options], [const.America_Chicago]*2)

    def test_create_activity_elpaso(self):
        """
        A valid activity in Elpaso should be created and the corresponding
        travel option entries should be populated successfully.
        """
        from_id = next(place_id_iter)
        to_id = next(place_id_iter)
        activity = activity_elpaso()

        client = APIClient()
        client.force_authenticate(user=self.user)
        r = client.put(reverse('create_update_activity', kwargs={'from_id': from_id, 'to_id': to_id}),
                       activity, format='json')
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

        activity_obj = Activity.objects.get(from_id=from_id, to_id=to_id)
        travel_options = TravelOption.objects.filter(activity_id=activity_obj.id)
        self.assertEqual(len(travel_options), 3)  # 3 entries should've been populated for this activity
        slots = [option.slot_id for option in travel_options]
        self.assertEqual(sorted(slots), [2, 95, 96])
        self.assertEqual([option.tz for option in travel_options], [const.America_Denver]*3)
        self.assertIn(const.WEEKDAY, [option.day_of_week for option in travel_options])
        self.assertIn(const.SATURDAY, [option.day_of_week for option in travel_options])

    def test_create_multiple_activities(self):
        """
        Multiple valid activities should be created and the corresponding
        travel option entries should be populated successfully.
        """
        from_id = next(place_id_iter)
        to_id = next(place_id_iter)
        activity = activity_tucson()

        client = APIClient()
        client.force_authenticate(user=self.user)
        r = client.put(reverse('create_update_activity', kwargs={'from_id': from_id, 'to_id': to_id}),
                       activity, format='json')
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

        from_id = next(place_id_iter)
        to_id = next(place_id_iter)
        activity = activity_austin()

        client = APIClient()
        client.force_authenticate(user=self.user)
        r = client.put(reverse('create_update_activity', kwargs={'from_id': from_id, 'to_id': to_id}),
                       activity, format='json')
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

        from_id = next(place_id_iter)
        to_id = next(place_id_iter)
        activity = activity_elpaso()

        client = APIClient()
        client.force_authenticate(user=self.user)
        r = client.put(reverse('create_update_activity', kwargs={'from_id': from_id, 'to_id': to_id}),
                       activity, format='json')
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

        r = client.get(reverse('activity_list'))
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json.loads(r.content.decode('utf-8'))), 3)

        options = TravelOption.objects.all()
        self.assertEqual(len(options), 8)  # total 8 travel options for these 3 activites

    def test_create_activity_invalid_latitude_upper_bound(self):
        """
        An activity with a invalid latitude value should be denied.
        """
        from_id = next(place_id_iter)
        to_id = next(place_id_iter)
        activity = activity_tucson()
        activity['from_lat'] = 90.1  # invalid

        client = APIClient()
        client.force_authenticate(user=self.user)
        r = client.put(reverse('create_update_activity', kwargs={'from_id': from_id, 'to_id': to_id}),
                       activity, format='json')
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertRegex(r.content.decode('utf-8'), "Latitude value must in between -90 and 90")

    def test_create_activity_invalid_latitude_lower_bound(self):
        """
        An activity with a invalid latitude value should be denied.
        """
        from_id = next(place_id_iter)
        to_id = next(place_id_iter)
        activity = activity_tucson()
        activity['to_lat'] = -90.1  # invalid

        client = APIClient()
        client.force_authenticate(user=self.user)
        r = client.put(reverse('create_update_activity', kwargs={'from_id': from_id, 'to_id': to_id}),
                       activity, format='json')
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertRegex(r.content.decode('utf-8'), "Latitude value must in between -90 and 90")

    def test_create_activity_invalid_longitude_upper_bound(self):
        """
        An activity with a invalid longitude value should be denied.
        """
        from_id = next(place_id_iter)
        to_id = next(place_id_iter)
        activity = activity_tucson()
        activity['from_lon'] = 180.1  # invalid

        client = APIClient()
        client.force_authenticate(user=self.user)
        r = client.put(reverse('create_update_activity', kwargs={'from_id': from_id, 'to_id': to_id}),
                       activity, format='json')
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertRegex(r.content.decode('utf-8'), "Longitude value must in between -180 and 180")

    def test_create_activity_invalid_longitude_lower_bound(self):
        """
        An activity with a invalid latitude value should be denied.
        """
        from_id = next(place_id_iter)
        to_id = next(place_id_iter)
        activity = activity_tucson()
        activity['to_lon'] = -180.1  # invalid

        client = APIClient()
        client.force_authenticate(user=self.user)
        r = client.put(reverse('create_update_activity', kwargs={'from_id': from_id, 'to_id': to_id}),
                       activity, format='json')
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertRegex(r.content.decode('utf-8'), "Longitude value must in between -180 and 180")

    def test_create_activity_missing_pattern_field(self):
        """
        An activity without a pattern field should be denied.
        """
        from_id = next(place_id_iter)
        to_id = next(place_id_iter)
        activity = {
            'from_lat': fixture.from_lat_tucson,
            'from_lon': fixture.from_lon_tucson,
            'to_lat': fixture.to_lat_tucson,
            'to_lon': fixture.to_lon_tucson,
            'purpose': const.WORK,
        }

        client = APIClient()
        client.force_authenticate(user=self.user)
        r = client.put(reverse('create_update_activity', kwargs={'from_id': from_id, 'to_id': to_id}),
                       activity, format='json')
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertRegex(r.content.decode('utf-8'), "patterns is required")

    def test_create_activity_invalid_purpose(self):
        """
        An activity with an invalid purpose should not be accepted.
        """
        from_id = next(place_id_iter)
        to_id = next(place_id_iter)
        activity = activity_tucson()
        activity['purpose'] = 'INVALID'

        client = APIClient()
        client.force_authenticate(user=self.user)
        r = client.put(reverse('create_update_activity', kwargs={'from_id': from_id, 'to_id': to_id}),
                       activity, format='json')
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertRegex(r.content.decode('utf-8'), "not a valid choice")

    def test_create_activity_prob_list_len(self):
        """
        Probability list in the request body should contain exactly 96 values.
        """
        from_id = next(place_id_iter)
        to_id = next(place_id_iter)
        activity = activity_prob_list_more_than_96()

        client = APIClient()
        client.force_authenticate(user=self.user)
        r = client.put(reverse('create_update_activity', kwargs={'from_id': from_id, 'to_id': to_id}),
                       activity, format='json')
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertRegex(r.content.decode('utf-8'), 'There should be exactly 96 probability values')

        activity = activity_prob_list_less_than_96()

        client = APIClient()
        client.force_authenticate(user=self.user)
        r = client.put(reverse('create_update_activity', kwargs={'from_id': from_id, 'to_id': to_id}),
                       activity, format='json')
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertRegex(r.content.decode('utf-8'), 'There should be exactly 96 probability values')

    def test_create_activity_prob_total_not_equals_100(self):
        """
        Sum of 96 values in probability list should equal to 100.
        """
        from_id = next(place_id_iter)
        to_id = next(place_id_iter)
        activity = activity_prob_total_above_100()

        client = APIClient()
        client.force_authenticate(user=self.user)
        r = client.put(reverse('create_update_activity', kwargs={'from_id': from_id, 'to_id': to_id}),
                       activity, format='json')
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertRegex(r.content.decode('utf-8'), 'The total of 96 probability values must not above 100')

        activity = activity_prob_total_below_100()

        client = APIClient()
        client.force_authenticate(user=self.user)
        r = client.put(reverse('create_update_activity', kwargs={'from_id': from_id, 'to_id': to_id}),
                       activity, format='json')
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertRegex(r.content.decode('utf-8'), 'The total of 96 probability values must not below 100')

    def test_create_activity_invalid_prob_value_type(self):
        """
        probability value should be either float or int, other types are not allowed.
        """
        from_id = next(place_id_iter)
        to_id = next(place_id_iter)
        activity = activity_invalid_prob_value_type()

        client = APIClient()
        client.force_authenticate(user=self.user)
        r = client.put(reverse('create_update_activity', kwargs={'from_id': from_id, 'to_id': to_id}),
                       activity, format='json')
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertRegex(r.content.decode('utf-8'), 'probability must be a float or int')

    def test_create_activity_prob_value_not_in_range(self):
        """
        The 96 values in probability list should be in the range of [0,100].
        """
        from_id = next(place_id_iter)
        to_id = next(place_id_iter)
        activity = activity_prob_value_below_zero()

        client = APIClient()
        client.force_authenticate(user=self.user)
        r = client.put(reverse('create_update_activity', kwargs={'from_id': from_id, 'to_id': to_id}),
                       activity, format='json')
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertRegex(r.content.decode('utf-8'), 'Probability value must be in between 0 and 100')

        activity = activity_prob_value_above_100()

        client = APIClient()
        client.force_authenticate(user=self.user)
        r = client.put(reverse('create_update_activity', kwargs={'from_id': from_id, 'to_id': to_id}),
                       activity, format='json')
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertRegex(r.content.decode('utf-8'), 'Probability value must be in between 0 and 100')

    def test_create_activity_same_from_id_to_id(self):
        """
        An activity with the same from_id and to_id should not be accepted.
        """
        from_id = next(place_id_iter)
        to_id = from_id  # not allowed
        activity = activity_tucson()

        client = APIClient()
        client.force_authenticate(user=self.user)
        r = client.put(reverse('create_update_activity', kwargs={'from_id': from_id, 'to_id': to_id}),
                       activity, format='json')
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertRegex(r.content.decode('utf-8'), "cannot be the same")

    def test_create_activity_missing_field_not_allowed(self):
        """
        An activity with a missing field should not be accepted.
        """
        from_id = next(place_id_iter)
        to_id = next(place_id_iter)
        activity = activity_tucson()
        activity.pop('from_lat')  # remove a required field

        client = APIClient()
        client.force_authenticate(user=self.user)
        r = client.put(reverse('create_update_activity', kwargs={'from_id': from_id, 'to_id': to_id}),
                       activity, format='json')
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertRegex(r.content.decode('utf-8'), 'This field is required')

    def test_update_activity(self):
        """
        When updating an activity, old entries of travel options should be deleted
        and new entries should be created.
        """
        from_id = next(place_id_iter)
        to_id = next(place_id_iter)
        activity = activity_tucson()

        client = APIClient()
        client.force_authenticate(user=self.user)
        r = client.put(reverse('create_update_activity', kwargs={'from_id': from_id, 'to_id': to_id}),
                       activity, format='json')
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

        activity = activity_tucson_update()
        client = APIClient()
        client.force_authenticate(user=self.user)
        r = client.put(reverse('create_update_activity', kwargs={'from_id': from_id, 'to_id': to_id}),
                       activity, format='json')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        activity_obj = Activity.objects.get(from_id=from_id, to_id=to_id)
        options = TravelOption.objects.filter(activity_id=activity_obj.id)
        self.assertEqual(len(options), 2)
        self.assertNotIn(const.WEEKDAY, [option.day_of_week for option in options])
        self.assertIn(const.THURSDAY, [option.day_of_week for option in options])

    def test_update_activity_invalid_update_request(self):
        """
        Invalid (missing field, wrong type, etc) update request should be denied and
        old entries of travel options should NOT be deleted.
        """
        from_id = next(place_id_iter)
        to_id = next(place_id_iter)
        activity = activity_tucson()

        client = APIClient()
        client.force_authenticate(user=self.user)
        r = client.put(reverse('create_update_activity', kwargs={'from_id': from_id, 'to_id': to_id}),
                       activity, format='json')
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

        activity = activity_tucson_update()
        activity['from_lat'] = 99  # make the activity invalid
        client = APIClient()
        client.force_authenticate(user=self.user)
        r = client.put(reverse('create_update_activity', kwargs={'from_id': from_id, 'to_id': to_id}),
                       activity, format='json')
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertRegex(r.content.decode('utf-8'), "Latitude value must in between -90 and 90")
        activity_obj = Activity.objects.get(from_id=from_id, to_id=to_id)
        options = TravelOption.objects.filter(activity_id=activity_obj.id)
        self.assertEqual(len(options), 3)  # old entries shouldn't be deleted

    def test_update_travel_options_drive(self):
        """
        Update of a valid drive option should be successful.
        """
        from_id = next(place_id_iter)
        to_id = next(place_id_iter)
        activity = activity_tucson()

        client = APIClient()
        client.force_authenticate(user=self.user)
        r = client.put(reverse('create_update_activity', kwargs={'from_id': from_id, 'to_id': to_id}),
                       activity, format='json')
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

        r = client.get(reverse('travel_options_by_day_of_week', kwargs={'day_of_week': const.WEEKDAY}))
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        travel_options = json.loads(r.content.decode('utf-8'))
        self.assertEqual(len(travel_options), 3)
        drive = {'drive': {'travel_time': 240, 'distance': 2}}
        for option in travel_options:
            r = client.put(reverse('update_travel_options', kwargs={'pk': option['id']}), drive, format='json')
            self.assertEqual(r.status_code, status.HTTP_200_OK)
            self.assertIn('drive', r.content.decode('utf-8'))
            self.assertIn('travel_time', json.loads(r.content.decode('utf-8'))['drive'])

            option_obj = TravelOption.objects.get(pk=option['id'])
            self.assertTrue(option_obj.drive == "{'travel_time': 240, 'distance': 2}" or
                            option_obj.drive == "{'distance': 2, 'travel_time': 240}")

    def test_update_travel_options_drive_missing_field_wrong_type(self):
        """
        A drive option with a missing field or wrong field type should not be accepted.
        """
        from_id = next(place_id_iter)
        to_id = next(place_id_iter)
        activity = activity_tucson()

        client = APIClient()
        client.force_authenticate(user=self.user)
        r = client.put(reverse('create_update_activity', kwargs={'from_id': from_id, 'to_id': to_id}),
                       activity, format='json')
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

        r = client.get(reverse('travel_options_by_day_of_week', kwargs={'day_of_week': const.WEEKDAY}))
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        travel_options = json.loads(r.content.decode('utf-8'))
        self.assertEqual(len(travel_options), 3)
        drive = {'drive': {'travel_time': 240}}
        for option in travel_options:
            r = client.put(reverse('update_travel_options', kwargs={'pk': option['id']}), drive, format='json')
            self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertRegex(r.content.decode('utf-8'), 'distance is missing in the drive option')

        drive = {'drive': {'travel_time': '240', 'distance': 2}}
        for option in travel_options:
            r = client.put(reverse('update_travel_options', kwargs={'pk': option['id']}), drive, format='json')
            self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertRegex(r.content.decode('utf-8'), 'travel_time must be a float or int')

    def test_update_travel_options_transit(self):
        """
        Update of a valid transit option should be successful.
        """
        from_id = next(place_id_iter)
        to_id = next(place_id_iter)
        activity = activity_tucson()

        client = APIClient()
        client.force_authenticate(user=self.user)
        r = client.put(reverse('create_update_activity', kwargs={'from_id': from_id, 'to_id': to_id}),
                       activity, format='json')
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

        r = client.get(reverse('travel_options_by_day_of_week', kwargs={'day_of_week': const.WEEKDAY}))
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        travel_options = json.loads(r.content.decode('utf-8'))
        self.assertEqual(len(travel_options), 3)
        transit = {'transit': {'travel_time': 240, 'wait_time': 2, 'cost': 125,
                               'walk_time_ingress': 44, 'walk_time_egress': 55}}
        for option in travel_options:
            r = client.put(reverse('update_travel_options', kwargs={'pk': option['id']}), transit, format='json')
            self.assertEqual(r.status_code, status.HTTP_200_OK)
            self.assertIn('transit', r.content.decode('utf-8'))
            self.assertIn('walk_time_ingress', json.loads(r.content.decode('utf-8'))['transit'])

            option_obj = TravelOption.objects.get(pk=option['id'])
            self.assertIn("'walk_time_egress': 55", option_obj.transit)

    def test_update_travel_options_transit_extra_field(self):
        """
        Update of a transit option with an extra field should not be accepted.
        """
        from_id = next(place_id_iter)
        to_id = next(place_id_iter)
        activity = activity_tucson()

        client = APIClient()
        client.force_authenticate(user=self.user)
        r = client.put(reverse('create_update_activity', kwargs={'from_id': from_id, 'to_id': to_id}),
                       activity, format='json')
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

        r = client.get(reverse('travel_options_by_day_of_week', kwargs={'day_of_week': const.WEEKDAY}))
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        travel_options = json.loads(r.content.decode('utf-8'))
        self.assertEqual(len(travel_options), 3)
        transit = {'transit': {'travel_time': 240, 'wait_time': 2, 'cost': 125,
                               'walk_time_ingress': 44, 'walk_time_egress': 55, 'extra_field': 'xyz'}}
        for option in travel_options:
            r = client.put(reverse('update_travel_options', kwargs={'pk': option['id']}), transit, format='json')
            self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertRegex(r.content.decode('utf-8'), 'transit option should contain exactly five fields')

    def test_update_travel_options_uber(self):
        """
        Update of a valid uber option should be successful.
        """
        from_id = next(place_id_iter)
        to_id = next(place_id_iter)
        activity = activity_tucson()

        client = APIClient()
        client.force_authenticate(user=self.user)
        r = client.put(reverse('create_update_activity', kwargs={'from_id': from_id, 'to_id': to_id}),
                       activity, format='json')
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

        r = client.get(reverse('travel_options_by_day_of_week', kwargs={'day_of_week': const.WEEKDAY}))
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        travel_options = json.loads(r.content.decode('utf-8'))
        self.assertEqual(len(travel_options), 3)
        uber = {
            'uber': {
                'uberx': {'travel_time': 240, 'wait_time': 20, 'cost': '$4-6'},
                'uberpool': {'travel_time': 480, 'wait_time': 40, 'cost': '$8-10'},
            },
        }
        for option in travel_options:
            r = client.put(reverse('update_travel_options', kwargs={'pk': option['id']}), uber, format='json')
            self.assertEqual(r.status_code, status.HTTP_200_OK)
            self.assertIn('uber', r.content.decode('utf-8'))
            self.assertIn('cost', json.loads(r.content.decode('utf-8'))['uber']['uberx'])

            option_obj = TravelOption.objects.get(pk=option['id'])
            self.assertIn("cost': '$4-6'", option_obj.uber)

    def test_update_travel_options_uber_uberxonly(self):
        """
        Update of a uber option with only uberx option should be successful.
        """
        from_id = next(place_id_iter)
        to_id = next(place_id_iter)
        activity = activity_tucson()

        client = APIClient()
        client.force_authenticate(user=self.user)
        r = client.put(reverse('create_update_activity', kwargs={'from_id': from_id, 'to_id': to_id}),
                       activity, format='json')
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

        r = client.get(reverse('travel_options_by_day_of_week', kwargs={'day_of_week': const.WEEKDAY}))
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        travel_options = json.loads(r.content.decode('utf-8'))
        self.assertEqual(len(travel_options), 3)
        uber = {
            'uber': {
                'uberx': {'travel_time': 240, 'wait_time': 20, 'cost': '$4-6'},
            },
        }
        for option in travel_options:
            r = client.put(reverse('update_travel_options', kwargs={'pk': option['id']}), uber, format='json')
            self.assertEqual(r.status_code, status.HTTP_200_OK)
            self.assertIn('uber', r.content.decode('utf-8'))
            self.assertIn('cost', json.loads(r.content.decode('utf-8'))['uber']['uberx'])
            self.assertNotIn('uberpool', r.content.decode('utf-8'))

            option_obj = TravelOption.objects.get(pk=option['id'])
            self.assertIn("cost': '$4-6'", option_obj.uber)

    def test_update_travel_options_uber_invalid(self):
        """
        Update of a invalid uber option should be denied.
        """
        from_id = next(place_id_iter)
        to_id = next(place_id_iter)
        activity = activity_tucson()

        client = APIClient()
        client.force_authenticate(user=self.user)
        r = client.put(reverse('create_update_activity', kwargs={'from_id': from_id, 'to_id': to_id}),
                       activity, format='json')
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

        r = client.get(reverse('travel_options_by_day_of_week', kwargs={'day_of_week': const.WEEKDAY}))
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        travel_options = json.loads(r.content.decode('utf-8'))
        self.assertEqual(len(travel_options), 3)
        uber = {
            'uber': {
                'ubernotx': {'travel_time': 240, 'wait_time': 20, 'cost': '$4-6'},
                'ubernotpool': {'travel_time': 480, 'wait_time': 40, 'cost': '$8-10'},
            },
        }
        for option in travel_options:
            r = client.put(reverse('update_travel_options', kwargs={'pk': option['id']}), uber, format='json')
            self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertRegex(r.content.decode('utf-8'), 'Neither uberx or uberpool are in the uber option')

    def test_update_travel_options_drive_transit(self):
        """
        Update of a valid drive and transit options together should be successful.
        """
        from_id = next(place_id_iter)
        to_id = next(place_id_iter)
        activity = activity_tucson()

        client = APIClient()
        client.force_authenticate(user=self.user)
        r = client.put(reverse('create_update_activity', kwargs={'from_id': from_id, 'to_id': to_id}),
                       activity, format='json')
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

        r = client.get(reverse('travel_options_by_day_of_week', kwargs={'day_of_week': const.WEEKDAY}))
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        travel_options = json.loads(r.content.decode('utf-8'))
        self.assertEqual(len(travel_options), 3)
        modes = {'transit': {'travel_time': 240, 'wait_time': 2, 'cost': 125,
                             'walk_time_ingress': 44, 'walk_time_egress': 55},
                 'drive': {'travel_time': 240, 'distance': 2}}
        for option in travel_options:
            r = client.put(reverse('update_travel_options', kwargs={'pk': option['id']}), modes, format='json')
            self.assertEqual(r.status_code, status.HTTP_200_OK)
            self.assertIn('transit', r.content.decode('utf-8'))
            self.assertIn('drive', r.content.decode('utf-8'))
            self.assertIn('distance', json.loads(r.content.decode('utf-8'))['drive'])
            self.assertIn('walk_time_ingress', json.loads(r.content.decode('utf-8'))['transit'])

            option_obj = TravelOption.objects.get(pk=option['id'])
            self.assertIn("'walk_time_egress': 55", option_obj.transit)
            self.assertIn("'distance': 2", option_obj.drive)

    def test_update_travel_options_invalid_mode(self):
        """
        Attempt of updating an invalid mode together should fail.
        """
        from_id = next(place_id_iter)
        to_id = next(place_id_iter)
        activity = activity_tucson()

        client = APIClient()
        client.force_authenticate(user=self.user)
        r = client.put(reverse('create_update_activity', kwargs={'from_id': from_id, 'to_id': to_id}),
                       activity, format='json')
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

        r = client.get(reverse('travel_options_by_day_of_week', kwargs={'day_of_week': const.WEEKDAY}))
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        travel_options = json.loads(r.content.decode('utf-8'))
        self.assertEqual(len(travel_options), 3)
        modes = {'transit': {'travel_time': 240, 'wait_time': 2, 'cost': 125,
                             'walk_time_ingress': 44, 'walk_time_egress': 55},
                 'drive': {'travel_time': 240, 'distance': 2},
                 'invalid mode': {'travel_time': 240}}
        for option in travel_options:
            r = client.put(reverse('update_travel_options', kwargs={'pk': option['id']}), modes, format='json')
            self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertRegex(r.content.decode('utf-8'), 'must be a subset of')

    def test_get_personalized_options(self):
        """
        All feasible personalized options for a valid activity should be returned.
        """
        from_id = next(place_id_iter)
        to_id = next(place_id_iter)
        activity = activity_tucson()

        client = APIClient()
        client.force_authenticate(user=self.user)
        r = client.put(reverse('create_update_activity', kwargs={'from_id': from_id, 'to_id': to_id}),
                       activity, format='json')
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

        activity_obj = Activity.objects.get(from_id=from_id, to_id=to_id)
        activity_obj.walk_time = 200
        activity_obj.bike_time = 100
        activity_obj.save()

        r = client.get(reverse('travel_options_by_day_of_week', kwargs={'day_of_week': const.WEEKDAY}))
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        travel_options = json.loads(r.content.decode('utf-8'))
        self.assertEqual(len(travel_options), 3)
        modes = {
            'transit': {'travel_time': 240, 'wait_time': 2, 'cost': 125,
                        'walk_time_ingress': 44, 'walk_time_egress': 55},
            'drive': {'travel_time': 240, 'distance': 2},
            'uber': {
                'uberx': {'travel_time': 240, 'wait_time': 20, 'cost': '$4-6'},
                'uberpool': {'travel_time': 480, 'wait_time': 40, 'cost': '$8-10'},
            },
        }
        for option in travel_options:
            r = client.put(reverse('update_travel_options', kwargs={'pk': option['id']}), modes, format='json')
            self.assertEqual(r.status_code, status.HTTP_200_OK)

        for slot_id in [1, 2, 3]:
            r = client.get(reverse('personalized_options', kwargs={'day_of_week': const.WEEKDAY,
                                                                   'from_id': from_id, 'to_id': to_id,
                                                                   'slot_id': slot_id}))
            self.assertEqual(r.status_code, status.HTTP_200_OK)
            # self.assertDictEqual(modes, json.loads(r.content.decode('utf-8')))
            options_dict = json.loads(r.content.decode('utf-8'))
            self.assertIn("distance", r.content.decode('utf-8'))
            self.assertEqual(type(options_dict), dict)
            self.assertEqual(options_dict['drive']['distance'], 2)
            self.assertEqual(options_dict['transit']['cost'], 125)
            self.assertEqual(options_dict['uber']['uberx']['wait_time'], 20)
            self.assertEqual(options_dict['uber']['uberpool']['cost'], '$8-10')

    def test_get_personalized_options_same_from_id_to_id(self):
        """
        An request to get personalized option of same from_id and to_id should be denied.
        """
        client = APIClient()
        client.force_authenticate(user=self.user)
        r = client.get(reverse('personalized_options', kwargs={'day_of_week': const.WEEKDAY,
                                                               'from_id': 1, 'to_id': 1,
                                                               'slot_id': 2}))
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertRegex(r.content.decode('utf-8'), 'cannot be the same')

    def test_get_personalized_options_slot_id_out_of_range(self):
        """
        An request to get personalized option in which slot_id is out of range should be denied.
        """
        client = APIClient()
        client.force_authenticate(user=self.user)
        r = client.get(reverse('personalized_options', kwargs={'day_of_week': const.WEEKDAY,
                                                               'from_id': 1, 'to_id': 2,
                                                               'slot_id': 0}))
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertRegex(r.content.decode('utf-8'), 'slot_id must be in the range of 1 to 96')

        r = client.get(reverse('personalized_options', kwargs={'day_of_week': const.WEEKDAY,
                                                               'from_id': 1, 'to_id': 2,
                                                               'slot_id': 97}))
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertRegex(r.content.decode('utf-8'), 'slot_id must be in the range of 1 to 96')

    def test_get_personalized_options_activity_not_exist(self):
        """
        An request to get personalized option of an activity that does not exist should be denied.
        """
        client = APIClient()
        client.force_authenticate(user=self.user)
        r = client.get(reverse('personalized_options', kwargs={'day_of_week': const.WEEKDAY,
                                                               'from_id': 1, 'to_id': 2,
                                                               'slot_id': 3}))
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertRegex(r.content.decode('utf-8'), 'does not exist')

    def test_get_personalized_options_entry_not_exist(self):
        """
        An request to get personalized option of an activity without a travel option entry
        identified by day_of_week and slot_id should be denied and informed.
        """
        from_id = next(place_id_iter)
        to_id = next(place_id_iter)
        activity = activity_tucson()

        client = APIClient()
        client.force_authenticate(user=self.user)
        r = client.put(reverse('create_update_activity', kwargs={'from_id': from_id, 'to_id': to_id}),
                       activity, format='json')
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

        r = client.get(reverse('personalized_options', kwargs={'day_of_week': const.WEEKDAY,
                                                               'from_id': from_id, 'to_id': to_id,
                                                               'slot_id': 4}))
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertRegex(r.content.decode('utf-8'), 'does not occur on')

    def test_get_personalized_options_zero_option(self):
        """
        An activity with zero personalized option should be returned with all options empty.
        """
        from_id = next(place_id_iter)
        to_id = next(place_id_iter)
        activity = activity_tucson()

        client = APIClient()
        client.force_authenticate(user=self.user)
        r = client.put(reverse('create_update_activity', kwargs={'from_id': from_id, 'to_id': to_id}),
                       activity, format='json')
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

        r = client.get(reverse('travel_options_by_day_of_week', kwargs={'day_of_week': const.WEEKDAY}))
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        for slot_id in [1, 2, 3]:
            r = client.get(reverse('personalized_options', kwargs={'day_of_week': const.WEEKDAY,
                                                                   'from_id': from_id, 'to_id': to_id,
                                                                   'slot_id': slot_id}))
            self.assertEqual(r.status_code, status.HTTP_200_OK)
            options_dict = json.loads(r.content.decode('utf-8'))
            self.assertIn("walk", r.content.decode('utf-8'))
            self.assertEqual(options_dict['drive'], {})
            self.assertEqual(options_dict['transit'], {})
            self.assertEqual(options_dict['uber'], {})
            self.assertEqual(options_dict['walk'], {})
            self.assertEqual(options_dict['bike'], {})

    def test_travel_options_by_day_of_week(self):
        """
        Given a day_of_week, travel_options_by_day_of_week view should return all
        travel options of the given day_of_week.
        """
        from_id = next(place_id_iter)
        to_id = next(place_id_iter)
        activity = activity_tucson()

        client = APIClient()
        client.force_authenticate(user=self.user)
        r = client.put(reverse('create_update_activity', kwargs={'from_id': from_id, 'to_id': to_id}),
                       activity, format='json')
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

        r = client.get(reverse('travel_options_by_day_of_week', kwargs={'day_of_week': const.WEEKDAY}))
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        options = json.loads(r.content.decode('utf-8'))
        self.assertEqual(len(options), 3)
        # self.assertEqual(sorted([option['id'] for option in options]), [1, 2, 3])
        self.assertEqual([option['activity'] for option in options], [1, 1, 1])
        self.assertEqual([option['slot_id'] for option in options], [1, 2, 3])

        from_id = next(place_id_iter)
        to_id = next(place_id_iter)
        activity = activity_austin()

        client = APIClient()
        client.force_authenticate(user=self.user)
        r = client.put(reverse('create_update_activity', kwargs={'from_id': from_id, 'to_id': to_id}),
                       activity, format='json')
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

        r = client.get(reverse('travel_options_by_day_of_week', kwargs={'day_of_week': const.MONDAY}))
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        options = json.loads(r.content.decode('utf-8'))
        self.assertEqual(len(options), 2)

        from_id = next(place_id_iter)
        to_id = next(place_id_iter)
        activity = activity_elpaso()

        client = APIClient()
        client.force_authenticate(user=self.user)
        r = client.put(reverse('create_update_activity', kwargs={'from_id': from_id, 'to_id': to_id}),
                       activity, format='json')
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

        r = client.get(reverse('travel_options_by_day_of_week', kwargs={'day_of_week': const.WEEKDAY}))
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        options = json.loads(r.content.decode('utf-8'))
        self.assertEqual(len(options), 5)

        r = client.get(reverse('travel_options_by_day_of_week', kwargs={'day_of_week': const.SATURDAY}))
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        options = json.loads(r.content.decode('utf-8'))
        self.assertEqual(len(options), 1)

    def test_travel_options_by_day_of_week_slot_tz(self):
        """
        Given a day_of_week, time slot and timezone, travel_options_by_day_of_week_slot_tz view
        should return all travel options matching the given parameters.
        """
        from_id = next(place_id_iter)
        to_id = next(place_id_iter)
        activity = activity_tucson()

        client = APIClient()
        client.force_authenticate(user=self.user)
        r = client.put(reverse('create_update_activity', kwargs={'from_id': from_id, 'to_id': to_id}),
                       activity, format='json')
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

        r = client.get(reverse('travel_options_by_day_of_week_slot_tz',
                               kwargs={'day_of_week': const.WEEKDAY, 'slot_id': 3,
                                       'tz': const.America_Phoenix}))
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        options = json.loads(r.content.decode('utf-8'))
        self.assertEqual(len(options), 1)
        # self.assertEqual(options[0]['id'], 3)
        self.assertEqual(options[0]['activity'], 1)
        self.assertEqual(options[0]['slot_id'], 3)

        r = client.get(reverse('activity_detail', kwargs={'pk': options[0]['activity']}))
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        activity = json.loads(r.content.decode('utf-8'))
        self.assertEqual(activity['id'], 1)
        self.assertEqual(activity['purpose'], const.WORK)
        self.assertEqual([activity['from_id'], activity['to_id']], [from_id, to_id])
        self.assertEqual([activity['from_lat'], activity['from_lon']],
                         [fixture.from_lat_tucson, fixture.from_lon_tucson])
        self.assertEqual([activity['to_lat'], activity['to_lon']],
                         [fixture.to_lat_tucson, fixture.to_lon_tucson])
        self.assertEqual(activity['walk_time'], None)
        self.assertEqual(activity['bike_time'], None)

