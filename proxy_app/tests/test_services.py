import unittest
from unittest.mock import patch
from proxy_pass.services import MercadoLibreAPIService, CacheService


class TestMercadoLibreAPIService(unittest.TestCase):

    @patch("proxy_pass.services.requests.get")
    def test_get_data_success(self, mock_get):
        mock_response = {"key": "value"}
        mock_get.return_value.json.return_value = mock_response
        response = MercadoLibreAPIService.get_data("/test", params={})
        self.assertEqual(response, mock_response)


class TestCacheService(unittest.TestCase):

    @patch("proxy_pass.services.cache.get")
    def test_get_from_cache_hit(self, mock_cache_get):
        mock_cache_get.return_value = '{"key": "value"}'
        data = CacheService.get_from_cache("test_key")
        self.assertEqual(data, {"key": "value"})
