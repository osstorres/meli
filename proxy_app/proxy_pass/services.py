from typing import Dict, Any


class MercadoLibreAPIService:
    BASE_URL = "https://api.mercadolibre.com"

    @classmethod
    def get_data(cls, path: str, params: Dict[str, str]) -> Dict:
        pass

    @classmethod
    def process_metadata(cls, request, cached: bool, status_code: int):
        pass


class CacheService:
    @staticmethod
    def get_from_cache(cache_key: str) -> Any | None:
        pass

    @staticmethod
    def store_in_cache(cache_key: str, data: Dict, expiration_time: int = 3600):
        pass
