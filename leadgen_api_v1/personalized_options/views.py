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
    activities = Activity.objects.all()
    serializer = ActivitySerializer(activities, many=True)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes((permissions.IsAuthenticated,))
def create_update_activity(request, from_id, to_id):
    if from_id == to_id:  # prevent request like /activity/1/1/
        return Response(
            {'Error': 'from_id ({}) and to_id ({}) cannot be the same!'.format(from_id, to_id)},
            status=status.HTTP_400_BAD_REQUEST
        )

    request.data['from_id'] = from_id
    request.data['to_id'] = to_id

    try:  # Update
        activity = Activity.objects.get(from_id=from_id, to_id=to_id)
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
    options = TravelOption.objects.filter(day_of_week=day_of_week)
    serializer = TravelOptionRetrieveSerializer(options, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def travel_options_by_day_of_week_slot_tz(request, day_of_week, slot_id, tz):
    options = TravelOption.objects.filter(day_of_week=day_of_week, slot_id=slot_id, tz=tz)
    serializer = TravelOptionRetrieveSerializer(options, many=True)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes((permissions.IsAuthenticated,))
def update_travel_options(request, pk):
    travel_option = TravelOption.objects.get(pk=pk)
    serializer = TravelOptionUpdateSerializer(travel_option, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
