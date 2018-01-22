from django.db import models
from django.core.validators import MaxValueValidator

from .constants import PURPOSE_CHOICES, DAY_OF_WEEK_CHOICES, MODE_CHOICES


class Activity(models.Model):
    """
    Activity patterns inferred from Metropia users' trip data.
    """

    purpose = models.CharField('Purpose of activity', max_length=2, choices=PURPOSE_CHOICES)
    day_of_week = models.CharField('Activity occurs in weekday or weekend',
                                   max_length=2, choices=DAY_OF_WEEK_CHOICES)
    from_id = models.BigIntegerField('ID of from location')
    to_id = models.BigIntegerField('ID of to location')
    from_lat = models.FloatField('Start latitude')
    from_lon = models.FloatField('Start longitude')
    to_lat = models.FloatField('End latitude')
    to_lon = models.FloatField('End longitude')
    probabilities = models.TextField('JSON format of probability values for 96 15-minute time slots')

    class Meta:
        indexes = [
            # To make table join with TravelOption on id fast
            models.Index(fields=['id'], name='activity_id_idx'),
            # To make "SELECT * from Activity where from_id=x and to_id=y" fast
            models.Index(fields=['from_id', 'to_id'], name='from_to_idx'),
        ]
        unique_together = ['from_id', 'to_id']


class TravelOption(models.Model):
    """
    Available travel options for activities
    """
    # Django creates BTree index on foreignkey field by default
    activity_id = models.ForeignKey(Activity, on_delete=models.CASCADE)
    mode = models.CharField(max_length=2, choices=MODE_CHOICES)
    wait_time = models.PositiveSmallIntegerField(default=0)
    travel_time = models.PositiveSmallIntegerField()
    # Use char field instead of int to adjust uber api's price range
    cost = models.CharField(max_length=10, default='')
    # Range: 1 to 96 for each time slot; other values are invalid
    # 0 is a special value indicating the option is time independent (walking, biking, uberx and uberPool)
    slot_id = models.PositiveSmallIntegerField(
        'ID of time slot this option corresponds to',
        default=0,
        validators=[MaxValueValidator(96, 'slot_id must be in the range of 0 - 96')])
