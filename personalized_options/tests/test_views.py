import json

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from .common import *
from ..models import Activity
import personalized_options.constants as const
import personalized_options.utils as utils


place_id_iter = utils.unique_place_id()


def create_activity_instance(purpose=const.WORK, day_of_week=const.WEEKDAY,
                             prob_list=utils.probability_list()):
    activity = {
        "from_id": next(place_id_iter),
        "to_id": next(place_id_iter),
        "from_lat": from_lat,
        "from_lon": from_lon,
        "to_lat": to_lat,
        "to_lon": to_lon,
        "purpose": purpose,
        "day_of_week": day_of_week,
        "probabilities": prob_list,
    }
    return activity


def set_up_user():
    username = 'alex'
    email = 'alex@hacker.com'
    password = 'alex_knows_nothing'
    return User.objects.create_user(username, email, password)


class ActivityListViewTest(APITestCase):

    def setUp(self):
        self.user = set_up_user()

    def test_get_list(self):
        data = {
            'from_id': 1,
            'to_id': 2,
            'from_lat': from_lat,
            'from_lon': from_lon,
            'to_lat': to_lat,
            'to_lon': to_lon,
            'purpose': 'W',
            'day_of_week': 'WD',
            'probabilities': utils.probability_list(),
        }
        Activity.objects.create(**data)

        client = APIClient()
        user = User.objects.get(username='alex')
        client.force_authenticate(user=user)
        response = client.get(reverse('create_activity'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json.loads(response.content.decode('utf-8'))), 1)

    def test_create_activity(self):
        """
        An activity with the correct and required field values should be created successfully.
        """
        data = {
            "from_id": next(place_id_iter),
            "to_id": next(place_id_iter),
            "from_lat": from_lat,
            "from_lon": from_lon,
            "to_lat": to_lat,
            "to_lon": to_lon,
            "purpose": "W",
            "day_of_week": "WD",
            "probabilities": utils.probability_list(),
        }
        client = APIClient()
        user = User.objects.get(username='alex')
        client.force_authenticate(user=user)
        response = client.post(reverse('create_activity'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_batch_of_activity(self):
        """
        All combinations of purpose and day_of_week should be created successfully.
        """
        client = APIClient()
        for purpose in const.PURPOSE_CHOICES:
            for day_of_week in const.DAY_OF_WEEK_CHOICES:
                data = {
                    "from_id": next(place_id_iter),
                    "to_id": next(place_id_iter),
                    "from_lat": from_lat,
                    "from_lon": from_lon,
                    "to_lat": to_lat,
                    "to_lon": to_lon,
                    "purpose": purpose[0],
                    "day_of_week": day_of_week[0],
                    "probabilities": utils.probability_list(),
                }
                user = User.objects.get(username='alex')
                client.force_authenticate(user=user)
                response = client.post(reverse('create_activity'), data, format='json')
                self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = client.get(reverse('create_activity'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json.loads(response.content.decode('utf-8'))),
                         len(const.PURPOSE_CHOICES) * len(const.DAY_OF_WEEK_CHOICES))

    def test_invalid_choices(self):
        """
        Invalid activity purpose and day_of_week should not be accepted.
        """
        client = APIClient()
        user = User.objects.get(username='alex')
        client.force_authenticate(user=user)

        activity = create_activity_instance(purpose='WH')  # an invalid activity purpose code
        response = client.post(reverse('create_activity'), activity, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertRegex(response.content.decode('utf-8'), "not a valid choice")

        activity = create_activity_instance(day_of_week='WA')  # an invalid day of week code
        response = client.post(reverse('create_activity'), activity, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertRegex(response.content.decode('utf-8'), "not a valid choice")

    def test_prob_list_len(self):
        """
        Probability list in the request body should contain exactly 96 values.
        """
        client = APIClient()
        user = User.objects.get(username='alex')
        client.force_authenticate(user=user)

        prob_list = utils.probability_list()
        prob_list.append(4.5)
        activity = create_activity_instance(prob_list=prob_list)
        response = client.post(reverse('create_activity'), activity, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertRegex(response.content.decode('utf-8'), 'There should be exactly 96 probability values')

    def test_prob_list_element_type(self):
        """
        Probability list must contain either float or int.
        """
        client = APIClient()
        user = User.objects.get(username='alex')
        client.force_authenticate(user=user)

        prob_list = utils.probability_list()
        prob_list[45] = str(prob_list[45])  # turn one element into a string
        activity = create_activity_instance(prob_list=prob_list)
        response = client.post(reverse('create_activity'), activity, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertRegex(response.content.decode('utf-8'), 'Probability value must be a float or int')

    def test_prob_list_total_equals_100(self):
        """
        Sum of 96 values in probability list should be equals to 100.
        """
        client = APIClient()
        user = User.objects.get(username='alex')
        client.force_authenticate(user=user)

        prob_list = utils.probability_list()
        prob_list[95] = 99.9  # make the last element big enough to let total exceed 100
        activity = create_activity_instance(prob_list=prob_list)
        response = client.post(reverse('create_activity'), activity, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertRegex(response.content.decode('utf-8'), 'The total of 96 probability values must sum up to 100')

    def test_from_id_to_id_must_unique_together(self):
        """
        from_id and to_id must be unique together across all records.
        """
        client = APIClient()
        user = User.objects.get(username='alex')
        client.force_authenticate(user=user)

        activity = create_activity_instance()
        response = client.post(reverse('create_activity'), activity, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Post the same activity again, shouldn't be allowed
        response = client.post(reverse('create_activity'), activity, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertRegex(response.content.decode('utf-8'), 'The fields from_id, to_id must make a unique set')

    def test_from_id_to_id_same_value_not_allowd(self):
        """
        from_id and to_id of an activity cannot be the same.
        """
        client = APIClient()
        user = User.objects.get(username='alex')
        client.force_authenticate(user=user)

        activity = create_activity_instance()
        activity['to_id'] = activity['from_id']  # make 2 IDs with the same value
        response = client.post(reverse('create_activity'), activity, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertRegex(response.content.decode('utf-8'), 'cannot be the same!')

    def test_missing_field_not_allowed(self):
        """
        An request with a missing field should not be allowed.
        """
        client = APIClient()
        user = User.objects.get(username='alex')
        client.force_authenticate(user=user)

        activity = create_activity_instance()
        activity.pop('to_lat', None)
        response = client.post(reverse('create_activity'), activity, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertRegex(response.content.decode('utf-8'), 'This field is required')


class ActivityUpdateViewTest(APITestCase):

    def setUp(self):
        self.user = set_up_user()

    def test_regular_update(self):
        """
        from_id and to_id of an activity cannot be the same.
        """
        client = APIClient()
        user = User.objects.get(username='alex')
        client.force_authenticate(user=user)

        activity = create_activity_instance()
        response = client.post(reverse('create_activity'), activity, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        from_id = activity['from_id']
        to_id = activity['to_id']
        activity.pop('from_id', None)
        activity.pop('to_id', None)
        activity['purpose'] = const.SHOPPING
        activity['day_of_week'] = const.WEEKEND
        response = client.put(reverse('update_activity', kwargs={'from_id': from_id, 'to_id': to_id}),
                              activity, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['purpose'], const.SHOPPING)
        self.assertEqual(response.data['day_of_week'], const.WEEKEND)

    def test_from_id_to_id_same_value_not_allowed(self):
        """
        from_id and to_id of an activity cannot be the same.
        """
        client = APIClient()
        user = User.objects.get(username='alex')
        client.force_authenticate(user=user)

        response = client.put(reverse('update_activity', kwargs={'from_id': 5, 'to_id': 5}),
                              {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_non_existing_activity(self):
        """
        Update a non-existing activity is not allowed
        """
        client = APIClient()
        user = User.objects.get(username='alex')
        client.force_authenticate(user=user)

        activity = create_activity_instance()
        from_id = activity['from_id']
        to_id = activity['to_id']
        activity.pop('from_id', None)
        activity.pop('to_id', None)
        response = client.put(reverse('update_activity', kwargs={'from_id': from_id, 'to_id': to_id}),
                              activity, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertRegex(response.content.decode('utf-8'), 'does not exist')
