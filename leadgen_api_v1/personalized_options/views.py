from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from .serializers import ActivitySerializer
from .serializers import TravelOptionRetrieveSerializer, TravelOptionUpdateSerializer
from .models import Activity, TravelOption


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def activity_list(request):
    """
    Get a list of activities.
    """
    activities = Activity.objects.all()
    serializer = ActivitySerializer(activities, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def activity_detail(request, pk):
    """
    Get an activity given its primary key.
    """
    activity = Activity.objects.get(pk=pk)
    serializer = ActivitySerializer(activity)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes((permissions.IsAuthenticated,))
def activity_walk_bike_time_update(request, pk, walk_time, bike_time):
    """
    Update walk time and bike time retrieved from OTP to database.
    """
    activity = Activity.objects.get(pk=pk)
    activity.walk_time = walk_time
    activity.bike_time = bike_time
    activity.save()
    return Response({'walk_time': walk_time, 'bike_time': bike_time}, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes((permissions.IsAuthenticated,))
def create_update_activity(request, from_id, to_id):
    """
    Create (if not exist) or Update (if exist) an activity.
    """
    if from_id == to_id:  # prevent request like /activity/1/1/
        return Response(
            {'Error': 'from_id ({}) and to_id ({}) cannot be the same!'.format(from_id, to_id)},
            status=status.HTTP_400_BAD_REQUEST
        )

    request.data['from_id'] = from_id
    request.data['to_id'] = to_id

    try:  # Update
        activity = Activity.objects.get(from_id=from_id, to_id=to_id)
        TravelOption.objects.filter(activity_id=activity.id).delete()  # delete old entries
        serializer = ActivitySerializer(activity, data=request.data)
        status_code = status.HTTP_200_OK

    except Activity.DoesNotExist:  # Create
        serializer = ActivitySerializer(data=request.data)
        status_code = status.HTTP_201_CREATED

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status_code)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def travel_options_by_day_of_week(request, day_of_week):
    """
    Get a list of travel options given `day_of_week`.
    """
    options = TravelOption.objects.filter(day_of_week=day_of_week)
    serializer = TravelOptionRetrieveSerializer(options, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def travel_options_by_day_of_week_slot_tz(request, day_of_week, slot_id, tz):
    """
    Get a list of travel options given `day_of_week`, `slot_id` and timezone `tz`.
    """
    options = TravelOption.objects.filter(day_of_week=day_of_week, slot_id=slot_id, tz=tz)
    serializer = TravelOptionRetrieveSerializer(options, many=True)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes((permissions.IsAuthenticated,))
def update_travel_options(request, pk):
    """
    Update a travel option whose primary key is `pk`.
    """
    valid_mode_set = {'drive', 'transit', 'uber'}
    request_mode_set = set(request.data.keys())
    if not request_mode_set.issubset(valid_mode_set):
        return Response(
            {'Error': 'The travel option you want to update must be a subset of {}.'.format(valid_mode_set)},
            status=status.HTTP_400_BAD_REQUEST
        )

    travel_option = TravelOption.objects.get(pk=pk)
    serializer = TravelOptionUpdateSerializer(travel_option, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def personalized_options(request, from_id, to_id, day_of_week, slot_id):
    """
    Get personalized travel options for an activity (identified by `from_id` and `to_id`)
    which occurred on `day_of_week` at specific time identified by `slot_id`.
    """
    if from_id == to_id:  # prevent request like /activity/1/1/
        return Response(
            {'Error': 'from_id ({}) and to_id ({}) cannot be the same!'.format(from_id, to_id)},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        activity = Activity.objects.get(from_id=from_id, to_id=to_id)
    except Activity.DoesNotExist:
        return Response(
            {'Error': 'The activity from location {} to location {} does not exist.'.format(from_id, to_id)},
            status=status.HTTP_400_BAD_REQUEST
        )

    option = TravelOption.objects.get(activity_id=activity.id, day_of_week=day_of_week, slot_id=slot_id)

    response = {
        'drive': {},
        'transit': {},
        'uber': {},
        'walk': {},
        'bike': {}
    }
    if option.drive is not '':
        response['drive'] = eval(option.drive)
    if option.transit is not '':
        response['transit'] = eval(option.transit)
    if option.uber is not '':
        response['uber'] = eval(option.uber)

    if activity.walk_time is not None:
        response['walk'] = {'travel_time': activity.walk_time}
    if activity.bike_time is not None:
        response['bike'] = {'travel_time': activity.bike_time}

    return Response(response)
