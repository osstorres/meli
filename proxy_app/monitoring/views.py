from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
import newrelic.agent

class HealthCheckApiView(APIView):
    permission_classes = []

    def get(self, request):
        newrelic.agent.ignore_transaction(flag=True)
        return Response("OK", status=status.HTTP_200_OK)
