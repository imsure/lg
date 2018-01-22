from .models import Activity

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

    for prob in probabilities:
        if not (isinstance(prob, float) or isinstance(prob, int)):
            raise serializers.ValidationError('Probability value must be a float. '
                                              'But {} is a {}'.format(prob, type(prob)))
        if not 0.0 <= prob <= 100.0:
            raise serializers.ValidationError('Probability value must be in between 0 and 100. '
                                              'But {} was given.'.format(prob))


class ActivitySerializer(serializers.ModelSerializer):
    probabilities = serializers.JSONField(validators=[validate_probabilities])

    def save(self, **kwargs):
        # Convert list to string
        probabilities = self.validated_data['probabilities']
        self.validated_data['probabilities'] = ','.join([str(p) for p in probabilities])
        super(ActivitySerializer, self).save(**kwargs)

    class Meta:
        model = Activity
        fields = '__all__'
