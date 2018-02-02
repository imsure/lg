from django.core.exceptions import ValidationError

from .models import Activity, TravelOption
from . import constants as const
from . import utils

from rest_framework import serializers

from timezonefinder import TimezoneFinder

Timezone_Finder = TimezoneFinder()


def check_if_int_or_float(value, name):
    if not (isinstance(value, float) or isinstance(value, int)):
        raise serializers.ValidationError(
            '{} must be a float or int. But {} is a {}'.format(name, value, type(value))
        )


def validate_probabilities(probabilities):
    """
    Check if `probabilities` is a JSON array with 96 probability values in float or int format.
    """
    # probabilities has been converted into a Python list from a JSON array via deserialization
    if len(probabilities) != 96:
        raise serializers.ValidationError("There should be exactly 96 probability values for the 96 " 
                                          "15-minute time slot. "
                                          "But {} values were provided.".format(len(probabilities)))

    prob_total = 0
    for prob in probabilities:
        check_if_int_or_float(prob, 'probability')
        if not 0.0 <= prob <= 100.0:
            raise serializers.ValidationError('Probability value must be in between 0 and 100. '
                                              'But {} was given.'.format(prob))

        prob_total += prob

    if prob_total < 99.9:
        raise serializers.ValidationError('The total of 96 probability values must not below 100. '
                                          'But the actual total {} is below 100.'.format(prob_total))
    if prob_total > 100.1:
        raise serializers.ValidationError('The total of 96 probability values must not above 100. '
                                          'But the actual total {} is above 100.'.format(prob_total))


def validate_patterns(patterns):
    day_of_week_set = set(patterns.keys())
    if len(patterns.keys()) > len(day_of_week_set):
        raise serializers.ValidationError('Day of week must be unique! But {} is given'.format(day_of_week_set))

    if not day_of_week_set.issubset(const.DAY_OF_WEEK_VALID_SET1) and \
            not day_of_week_set.issubset(const.DAY_OF_WEEK_VALID_SET2) and \
            not day_of_week_set.issubset(const.DAY_OF_WEEK_VALID_SET3) and \
            not day_of_week_set.issubset(const.DAY_OF_WEEK_VALID_SET4):
        raise serializers.ValidationError('{} is not a valid set!'.format(day_of_week_set))

    for key in patterns.keys():
        validate_probabilities(patterns[key])


def create_travel_option_entry(activity, day_of_week, slot_id, tz):
    try:
        TravelOption.objects.get(activity__pk=activity.id, day_of_week=day_of_week, slot_id=slot_id)
    except TravelOption.DoesNotExist:
        entry = TravelOption(activity=activity, day_of_week=day_of_week, slot_id=slot_id, tz=tz)
        try:
            entry.full_clean()
            entry.save()
        except ValidationError:
            pass  # TODO: log the message


class ActivitySerializer(serializers.ModelSerializer):
    patterns = serializers.JSONField(validators=[validate_patterns], required=False)

    def save(self, **kwargs):
        pat = self.validated_data.pop('patterns')

        from_lon = self.validated_data['from_lon']
        from_lat = self.validated_data['from_lat']
        # to_lon = self.validated_data['to_lon']
        # to_lat = self.validated_data['to_lat']
        tz = Timezone_Finder.timezone_at(lng=from_lon, lat=from_lat)
        tz = const.TZ_MAP[tz]

        # TODO: better run this asynchronously
        # walk_time, bike_time = utils.otp_walk_bike_time(from_lat, from_lon, to_lat, to_lon, tz)
        # self.validated_data['walk_time'] = walk_time
        # self.validated_data['bike_time'] = bike_time

        super().save(**kwargs)

        activity = self.instance
        for day_of_week, prob_list in pat.items():
            for slot_id, prob in enumerate(prob_list, start=1):
                if prob >= const.PROB_THRESHOLD:  # TODO: use the actual value
                    create_travel_option_entry(activity, day_of_week, slot_id, tz)

    class Meta:
        model = Activity
        fields = '__all__'


class TravelOptionRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = TravelOption
        fields = ('id', 'activity', 'slot_id',)
        read_only_fields = ('id', 'activity', 'slot_id',)


def validate_drive_option(drive):
    """
    drive option should be in JSON format with two fields:
    {
        "travel_time": 123 (in seconds),
        "distance": 5.6 (in miles)
    }
    """
    if 'travel_time' not in drive:
        raise serializers.ValidationError("travel_time is missing in the drive option.")

    if 'distance' not in drive:
        raise serializers.ValidationError("distance is missing in the drive option.")

    if len(drive.keys()) != 2:
        raise serializers.ValidationError("drive option should contain exactly two fields. "
                                          "But {} fields are given.".format(len(drive.keys())))

    travel_time = drive['travel_time']
    distance = drive['distance']
    check_if_int_or_float(travel_time, 'travel_time')
    check_if_int_or_float(distance, 'distance')


def validate_transit_option(transit):
    """
    transit option should be in JSON format with five fields:
    {
        "travel_time": 123 (in seconds),
        "wait_time": 456 (in seconds),
        "cost": 78 (in cents),
        "walk_time_ingress": 89 (in seconds),
        "walk_time_egress": 90 (in seconds)
    }
    """
    if 'travel_time' not in transit:
        raise serializers.ValidationError("travel_time is missing in the transit option.")

    if 'wait_time' not in transit:
        raise serializers.ValidationError("wait_time is missing in the transit option.")

    if 'cost' not in transit:
        raise serializers.ValidationError("cost is missing in the transit option.")

    if 'walk_time_ingress' not in transit:
        raise serializers.ValidationError("walk_time_ingress is missing in the transit option.")

    if 'walk_time_egress' not in transit:
        raise serializers.ValidationError("walk_time_egress is missing in the transit option.")

    if len(transit.keys()) != 5:
        raise serializers.ValidationError("transit option should contain exactly five fields. "
                                          "But {} fields are given.".format(len(transit.keys())))

    check_if_int_or_float(transit['travel_time'], 'travel_time')
    check_if_int_or_float(transit['wait_time'], 'wait_time')
    check_if_int_or_float(transit['cost'], 'cost')
    check_if_int_or_float(transit['walk_time_ingress'], 'walk_time_ingress')
    check_if_int_or_float(transit['walk_time_egress'], 'walk_time_egress')


def validate_uber_option(uber):
    """
    uber option should be in JSON format with two fields:
    {
        "travel_time": 123 (in seconds),
        "wait_time": 456 (in seconds),
        "cost": "$7-10" (string)
    }
    """
    if 'travel_time' not in uber:
        raise serializers.ValidationError("travel_time is missing in the uber option.")

    if 'wait_time' not in uber:
        raise serializers.ValidationError("wait_time is missing in the uber option.")

    if 'cost' not in uber:
        raise serializers.ValidationError("cost is missing in the uber option.")

    check_if_int_or_float(uber['travel_time'], 'travel_time')
    check_if_int_or_float(uber['wait_time'], 'wait_time')


class TravelOptionUpdateSerializer(serializers.ModelSerializer):
    drive = serializers.JSONField(validators=[validate_drive_option])
    transit = serializers.JSONField(validators=[validate_transit_option])
    uber = serializers.JSONField(validators=[validate_uber_option])

    class Meta:
        model = TravelOption
        fields = ('drive', 'transit', 'uber',)
