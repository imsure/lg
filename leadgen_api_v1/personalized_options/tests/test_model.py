from django.core.exceptions import ValidationError

from rest_framework.test import APITestCase

from . import fixture
from ..models import Activity


class ActivityModelTests(APITestCase):

    def test_create_a_valid_activity(self):
        """
        Test if a valid activity can be created
        """
        data = {
            'from_id': 1,
            'to_id': 2,
            'from_lat': fixture.from_lat_tucson,
            'from_lon': fixture.from_lon_tucson,
            'to_lat': fixture.to_lat_tucson,
            'to_lon': fixture.to_lon_tucson,
            'purpose': 'W',
        }
        activity = Activity.objects.create(**data)
        activity.full_clean()  # invoke model validation
        self.assertEqual(Activity.objects.count(), 1)
        self.assertQuerysetEqual([activity], ['<Activity: Activity object (1)>'])

    def test_unique_from_to_pair(self):
        """
        from_id and to_id must be unique together.
        """
        data = {
            'from_id': 1,
            'to_id': 2,
            'from_lat': fixture.from_lat_tucson,
            'from_lon': fixture.from_lon_tucson,
            'to_lat': fixture.to_lat_tucson,
            'to_lon': fixture.to_lon_tucson,
            'purpose': 'W',
        }
        activity = Activity.objects.create(**data)
        activity.full_clean()  # invoke model validation
        same_activity = Activity(**data)  # try to create an exact same activity
        with self.assertRaises(ValidationError) as context:
            same_activity.full_clean()

        self.assertRegex(str(context.exception),
                         'Activity with this ID of from location and ID of to location already exists.')

    def test_from_to_id_same(self):
        """
        from_id and to_id of an activity cannot be the same
        """
        data = {
            'from_id': 1,
            'to_id': 1,
            'from_lat': fixture.from_lat_tucson,
            'from_lon': fixture.from_lon_tucson,
            'to_lat': fixture.to_lat_tucson,
            'to_lon': fixture.to_lon_tucson,
            'purpose': 'W',
        }
        with self.assertRaises(ValidationError) as context:
            activity = Activity.objects.create(**data)
            activity.full_clean()  # invoke model validation

        self.assertRegex(repr(context.exception), 'cannot be the same!')
