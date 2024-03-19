from typing import Dict, Any
from django.core.cache import cache
import requests
import json
from operations.tasks import send_metadata_to_sqs


class MercadoLibreAPIService:
    BASE_URL = "https://api.mercadolibre.com"

    @classmethod
    def get_data(cls, path: str, params: Dict[str, str]) -> Dict:
        """
        Make a GET request to the MercadoLibre API.
        """
        url = f"{cls.BASE_URL}{path}"
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise exception if request fails
        return response.json()

    @classmethod
    def process_metadata(cls, request, cached: bool, status_code: int):
        send_metadata_to_sqs.delay(
            request.META.get("REMOTE_ADDR"),
            request.method,
            request.path,
            dict(request.query_params),
            dict(request.headers),
            cached,
            status_code,
        )


class CacheService:
    @staticmethod
    def get_from_cache(cache_key: str) -> Any | None:
        """
        Retrieve data from cache.
        """
        if cached_data := cache.get(cache_key):
            return json.loads(cached_data)
        return None

    @staticmethod
    def store_in_cache(cache_key: str, data: Dict, expiration_time: int = 3600):
        """
        Store data in cache.
        """
        cache.set(cache_key, json.dumps(data), expiration_time)
