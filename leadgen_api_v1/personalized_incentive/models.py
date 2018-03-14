from django.db import models


class IncentiveParams(models.Model):
    """
    Incentive parameters for each metropia user
    """
    metropia_id = models.IntegerField(primary_key=True)
    alpha = models.FloatField()
    beta = models.FloatField()
    gamma = models.FloatField()
    incentives = models.TextField()
