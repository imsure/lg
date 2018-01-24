from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from .serializers import ActivitySerializer
from .models import Activity


@api_view(['GET', 'POST'])
@permission_classes((permissions.IsAuthenticated,))
def activity_list(request):
    if request.method == 'GET':
        activities = Activity.objects.all()
        serializer = ActivitySerializer(activities, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ActivitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes((permissions.IsAuthenticated,))
def update_activity(request, from_id, to_id):
    if from_id == to_id:  # prevent request like /activity/1/1/
        return Response({'Error': 'from_id ({}) and to_id ({}) cannot be the same!'.format(from_id, to_id)},
                        status=status.HTTP_400_BAD_REQUEST)

    try:
        activity = Activity.objects.get(from_id=from_id, to_id=to_id)
        request.data['from_id'] = from_id
        request.data['to_id'] = to_id
        serializer = ActivitySerializer(activity, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Activity.DoesNotExist:
        msg = {
            "Error": "Activity from location {} to location {} " 
                     "you are trying to update does not exist!".format(from_id, to_id)
        }
        return Response(msg, status.HTTP_404_NOT_FOUND)
