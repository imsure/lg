from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError

from .constants import PURPOSE_CHOICES, DAY_OF_WEEK_CHOICES, TZ_CHOICES


class Activity(models.Model):
    """
    Activity patterns inferred from Metropia users' trip data.
    """

    purpose = models.CharField('Purpose of activity', max_length=2, choices=PURPOSE_CHOICES)
    from_id = models.IntegerField('ID of from location')
    to_id = models.IntegerField('ID of to location')
    from_lat = models.FloatField('Start latitude')
    from_lon = models.FloatField('Start longitude')
    to_lat = models.FloatField('End latitude')
    to_lon = models.FloatField('End longitude')
    # patterns = models.TextField('Activity patterns in JSON format')
    walk_time = models.PositiveSmallIntegerField(blank=True, null=True)
    bike_time = models.PositiveSmallIntegerField(blank=True, null=True)

    def clean(self):  # model-wide validation
        if self.from_id == self.to_id:
            raise ValidationError('from_id ({}) and to_id ({}) cannot be the same!'.format(self.from_id, self.to_id))

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
    Available travel options for an activity
    """
    # Django creates BTree index on foreignkey field by default
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    day_of_week = models.CharField('Activity occurs in which day',
                                   max_length=2, choices=DAY_OF_WEEK_CHOICES)
    # Range: 1 to 96 for each time slot; other values are invalid
    slot_id = models.PositiveSmallIntegerField(
        'ID of time slot this option corresponds to',
        validators=[MinValueValidator(1), MaxValueValidator(96)]
    )
    tz = models.CharField('Time Zone', max_length=2, choices=TZ_CHOICES)
    drive = models.CharField(max_length=100, blank=True, default='')
    transit = models.CharField(max_length=200, blank=True, default='')
    uber = models.CharField(max_length=200, blank=True, default='')

    class Meta:
        unique_together = ['activity', 'day_of_week', 'slot_id']
        indexes = [
            models.Index(fields=['day_of_week', 'slot_id', 'tz'], name='day_of_week_slot_tz_idx')
        ]
