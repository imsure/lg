from django.http import Http404

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .serializers import IncentiveParamsSerializer
from .serializers import IncentivePointsSerializer
from .models import IncentiveParams
from . import default


def minutes2slot_id(minutes):
    """
    Convert time of day in total # of minutes to one of 96 time slot ID

    :param minutes: time of day in total # of minutes
    :return: slot id within [1, 96]
    """
    if minutes >= 1440:  # 24 * 60 = 1440
        minutes -= 1440
    return minutes // 15 + 1


def validate_from_to_cities(from_city, to_city):
    is_valid = True
    msg = None
    sts = status.HTTP_200_OK

    if not isinstance(from_city, str):
        is_valid = False
        msg = 'from_city {} is not a string!'.format(from_city)
        sts = status.HTTP_400_BAD_REQUEST
        return is_valid, msg, sts

    if not isinstance(to_city, str):
        is_valid = False
        msg = 'to_city {} is not a string!'.format(to_city)
        sts = status.HTTP_400_BAD_REQUEST
        return is_valid, msg, sts

    cities = default.incentives.keys()
    if from_city not in cities:
        is_valid = False
        msg = 'Support of from_city {} is not available now'.format(from_city)
        sts = status.HTTP_404_NOT_FOUND
        return is_valid, msg, sts

    if to_city not in cities:
        is_valid = False
        msg = 'Support of to_city {} is not available now'.format(to_city)
        sts = status.HTTP_404_NOT_FOUND
        return is_valid, msg, sts

    if from_city != to_city and '{}-{}'.format(from_city, to_city) not in cities:
        is_valid = False
        msg = 'Support of from {} to {} is not available now'.format(from_city, to_city)
        sts = status.HTTP_404_NOT_FOUND
        return is_valid, msg, sts

    return is_valid, msg, sts


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def personalized_incentive(request, metropia_id, from_city, to_city):
    point_serializer = IncentivePointsSerializer(data=request.data)
    if not point_serializer.is_valid():
        return Response(point_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    slot_id = minutes2slot_id(request.data['minutes']) - 1
    energy = request.data['energy']
    congestion_level = request.data['congestion_level']

    try:
        incentive_params = IncentiveParams.objects.get(pk=metropia_id)
        alpha = incentive_params.alpha
        beta = incentive_params.beta
        gamma = incentive_params.gamma
        incentives = eval(incentive_params.incentives)
        incentive = incentives[slot_id]
    except IncentiveParams.DoesNotExist:
        is_valid, msg, sts = validate_from_to_cities(from_city, to_city)
        if not is_valid:
            return Response({'msg': msg}, status=sts)

        if from_city == to_city:
            city_key = from_city
        else:
            city_key = '{}-{}'.format(from_city, to_city)

        alpha = default.alpha
        beta = default.beta
        gamma = default.gamma
        incentive = default.incentives[city_key][slot_id]

    points = alpha * incentive + beta * energy + gamma * congestion_level
    return Response(
        {'alpha': alpha, 'beta': beta, 'gamma': gamma, 'slot_id': slot_id, 'incentive': incentive,
         'points': points, 'energy': energy, 'congestion_level': congestion_level},
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def personalized_unit(request, metropia_id):
    try:
        incentive_params = IncentiveParams.objects.get(pk=metropia_id)
        case_id = incentive_params.case_id
        return Response({'unit': default.unit_map[case_id]}, status=status.HTTP_200_OK)
    except IncentiveParams.DoesNotExist:
        return Response({'unit': default.unit_map[default.case_id]}, status=status.HTTP_200_OK)


class IncentiveParamsDetail(APIView):
    """
    Retrieve, create or update incentive params for a metropia user.
    """
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get_object(self, metropia_id):
        try:
            return IncentiveParams.objects.get(pk=metropia_id)
        except IncentiveParams.DoesNotExist:
            raise Http404

    def get(self, request, metropia_id):
        incentive_params = self.get_object(metropia_id)
        serializer = IncentiveParamsSerializer(incentive_params)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, metropia_id):
        request.data['metropia_id'] = metropia_id
        try:
            incentive_obj = IncentiveParams.objects.get(pk=metropia_id)
            serializer = IncentiveParamsSerializer(incentive_obj, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        except IncentiveParams.DoesNotExist:
            serializer = IncentiveParamsSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
