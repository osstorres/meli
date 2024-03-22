from rest_framework.test import APITestCase
from django.test import override_settings
from unittest.mock import patch
from proxy_pass.services import CacheService, MercadoLibreAPIService
import requests


class TestProxyView(APITestCase):

    @patch("proxy_pass.views.CacheService.get_from_cache")
    @patch("proxy_pass.views.MercadoLibreAPIService.get_data")
    @patch("proxy_pass.views.CacheService.store_in_cache")
    def test_proxy_view_cache_hit(
        self, mock_store_in_cache, mock_get_data, mock_get_from_cache
    ):
        # Set up mocks
        mock_get_from_cache.return_value = {"key": "value"}
        mock_get_data.side_effect = Exception("Should not call get_data if cache hit")

        # Make request
        response = self.client.get("/categories/MLA5725")

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"key": "value"})
        mock_get_from_cache.assert_called_once_with("/categories/MLA5725")
        mock_get_data.assert_not_called()
        mock_store_in_cache.assert_not_called()

    @patch("proxy_pass.views.CacheService.get_from_cache")
    @patch("proxy_pass.views.MercadoLibreAPIService.get_data")
    @patch("proxy_pass.views.CacheService.store_in_cache")
    def test_proxy_view_cache_miss(
        self, mock_store_in_cache, mock_get_data, mock_get_from_cache
    ):
        # Set up mocks
        mock_get_from_cache.return_value = None
        mock_get_data.return_value = ({"key": "value"}, 200)

        # Make request
        response = self.client.get("/categories/MLA5725")

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"key": "value"})
        mock_get_from_cache.assert_called_once_with("/categories/MLA5725")
        mock_get_data.assert_called_once_with("/categories/MLA5725", {})
        mock_store_in_cache.assert_called_once_with(
            "/categories/MLA5725", {"key": "value"}
        )

    @patch("proxy_pass.views.CacheService.get_from_cache")
    @patch("proxy_pass.views.MercadoLibreAPIService.get_data")
    @patch("proxy_pass.views.CacheService.store_in_cache")
    def test_proxy_view_api_failure(
        self, mock_store_in_cache, mock_get_data, mock_get_from_cache
    ):
        # Set up mocks
        mock_get_from_cache.return_value = None
        mock_get_data.side_effect = requests.RequestException("API Error")

        # Make request
        response = self.client.get("/categories/MLA5725")

        # Assertions
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"error": "API Error"})
        mock_get_from_cache.assert_called_once_with("/categories/MLA5725")
        mock_get_data.assert_called_once_with("/categories/MLA5725", {})
        mock_store_in_cache.assert_not_called()

    @override_settings(
        BLOCKED_IPS=[
            "127.0.0.1",
        ]
    )
    def test_proxy_block_ip(self):
        response = self.client.get("/categories/MLA5725")
        self.assertEqual(response.status_code, 403)

    def test_proxy_view_failure_1(self):
        response = self.client.get("/categories/MLA5725556asd")
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.data)

    def test_rate_limit(self):
        for request in range(1, 7):
            response = self.client.post("/any_path/")
            if request == 6:
                self.assertEqual(
                    response.status_code,
                    403,
                    {"detail": "You do not have permission to perform this action."},
                )
            else:
                self.assertEqual(response.status_code, 201, "OK")

    def test_not_cached_url(self):
        # Testing a URL that is not allowed for caching
        path_key = "/url_not_cached/test"
        self.client.get(path_key)
        self.assertEqual(CacheService.get_from_cache(cache_key=path_key), None)

    def test_another_cached_url(self):
        path_key = "/sites/MLA/"
        self.client.get(path_key)
        self.assertIsNotNone(CacheService.get_from_cache(cache_key=path_key))
