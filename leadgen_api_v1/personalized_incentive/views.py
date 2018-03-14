from django.http import Http404

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions, authentication
from rest_framework.views import APIView

from .serializers import IncentiveParamsSerializer
from .models import IncentiveParams


class IncentiveParamsDetail(APIView):
    """
    Retrieve, create or update incentive params for a metropia user.
    """
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
