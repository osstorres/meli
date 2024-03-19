from rest_framework.views import APIView


class ProxyView(APIView):
    def get(self, request, *args, **kwargs):
        pass
