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
        pass
