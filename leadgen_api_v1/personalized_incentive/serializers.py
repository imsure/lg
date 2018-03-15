from rest_framework import serializers

from .models import IncentiveParams
from .models import IncentivePoints


def check_if_int_or_float(value, name):
    if not (isinstance(value, float) or isinstance(value, int)):
        raise serializers.ValidationError(
            '{} must be a float or int. But {} is a {}'.format(name, value, type(value))
        )


def validate_incentives(incentives):
    """
    Check if `incentives` is a JSON array with 96 values in float or int.
    """
    # incentives has been converted into a Python list from a JSON array via deserialization
    if len(incentives) != 96:
        raise serializers.ValidationError("There should be exactly 96 incentives values for the 96 "
                                          "15-minute time slot. "
                                          "But {} values were provided.".format(len(incentives)))

    for incentive in incentives:
        check_if_int_or_float(incentive, 'incentive')


class IncentiveParamsSerializer(serializers.ModelSerializer):
    """
    Serializer for IncentiveParams model.
    """
    incentives = serializers.JSONField(validators=[validate_incentives])

    class Meta:
        model = IncentiveParams
        fields = '__all__'


class IncentivePointsSerializer(serializers.ModelSerializer):
    """
    Serializer for IncentivePoints model.
    """

    def save(self, **kwargs):
        pass

    class Meta:
        model = IncentivePoints
        fields = '__all__'
