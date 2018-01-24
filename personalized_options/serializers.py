from .models import Activity

from django.core.exceptions import ValidationError
from rest_framework import serializers


def validate_probabilities(probabilities):
    """
    Check if `probabilities` is a JSON array with 96 probability values in float format.
    """
    # probabilities has been converted into a Python list from a JSON array via deserialization
    if len(probabilities) != 96:
        raise serializers.ValidationError("There should be exactly 96 probability values for the 96 " 
                                          "15-minute time slot, no more, no less. "
                                          "But {} values were provided.".format(len(probabilities)))

    prob_total = 0
    for prob in probabilities:
        if not (isinstance(prob, float) or isinstance(prob, int)):
            raise serializers.ValidationError('Probability value must be a float or int. '
                                              'But {} is a {}'.format(prob, type(prob)))
        if not 0.0 <= prob <= 100.0:
            raise serializers.ValidationError('Probability value must be in between 0 and 100. '
                                              'But {} was given.'.format(prob))

        prob_total += prob

    if prob_total < 99.9:
        raise serializers.ValidationError('The total of 96 probability values must sum up to 100. '
                                          'But the actual total is below 100, which is {}'.format(prob_total))
    if prob_total > 100.1:
        raise serializers.ValidationError('The total of 96 probability values must not above 100. '
                                          'But the actual total is above 100, which is {}'.format(prob_total))


class ActivitySerializer(serializers.ModelSerializer):
    probabilities = serializers.JSONField(validators=[validate_probabilities])

    def validate(self, attrs):
        """
        Check if from_id and to_id are different.
        """
        if attrs['from_id'] == attrs['to_id']:
            raise ValidationError('from_id ({}) and to_id ({}) cannot be the same!'
                                  .format(attrs['from_id'], attrs['to_id']))
        return attrs

    def save(self, **kwargs):
        # Convert list to string
        probabilities = self.validated_data['probabilities']
        self.validated_data['probabilities'] = ','.join([str(p) for p in probabilities])
        super(ActivitySerializer, self).save(**kwargs)

    class Meta:
        model = Activity
        fields = '__all__'
