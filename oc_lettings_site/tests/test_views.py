from django.test import TestCase
from django.urls import reverse


class IndexPageTest(TestCase):
    def test_index_page_returns_200(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_index_page_contains_titles(self):
        response = self.client.get(reverse("index"))
        self.assertContains(response, "Holiday Homes")
        self.assertContains(response, "Profiles")
        self.assertContains(response, "Lettings")
