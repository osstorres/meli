from rest_framework.views import APIView
from rest_framework.response import Response
from .services import CacheService, MercadoLibreAPIService
import requests
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
from django.conf import settings


@method_decorator(
    ratelimit(key="ip", rate="5/m", method=["POST"], block=True), name="post"
)
@method_decorator(
    ratelimit(key="ip", rate="50/m", method="GET", block=True), name="get"
)
class ProxyView(APIView):
    def get(self, request, *args, **kwargs):
        path = request.path
        params = request.query_params
        cache_key = f"{path}"

        # Attempt to retrieve data from cache
        cached_data = CacheService.get_from_cache(cache_key)
        if cached_data:
            MercadoLibreAPIService.process_metadata(request, True, 200)
            return Response(cached_data)

        # Fetch data from MercadoLibre API
        try:
            data, status = MercadoLibreAPIService.get_data(path, params)
            MercadoLibreAPIService.process_metadata(request, False, status)
            CacheService.store_in_cache(cache_key, data)
            return Response(data)
        except requests.RequestException as e:
            status = e.status_code if hasattr(e, "status_code") else 400
            MercadoLibreAPIService.process_metadata(request, False, status)
            return Response({"error": str(e)}, status=status)

    def post(self, request, *args, **kwargs):
        # Testing rate limit post method by ip:)
        return Response("OK", status=201)
