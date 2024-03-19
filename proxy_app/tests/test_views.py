from rest_framework.test import APITestCase


class TestProxyView(APITestCase):

    def test_proxy_view_success(self):

        response = self.client.get("/categories/MLA5725")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("id"), "MLA5725")

    def test_proxy_view_failure(self):

        response = self.client.get("/categories/MLA5725556asd")
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.data)
