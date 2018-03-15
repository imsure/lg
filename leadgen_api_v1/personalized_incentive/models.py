from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class IncentiveParams(models.Model):
    """
    Incentive parameters for each metropia user
    """
    metropia_id = models.IntegerField(primary_key=True)
    alpha = models.FloatField()
    beta = models.FloatField()
    gamma = models.FloatField()
    incentives = models.TextField()


class IncentivePoints(models.Model):
    """
    Incentive points calculated for each user.
    This is a dummy table, we do not actually store these data, but we make use of
    serializer to do validation and overwrite save method to calculate points.
    """
    minutes = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1440)])
    energy = models.FloatField()
    congestion_level = models.FloatField()
