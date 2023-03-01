from django.test import TestCase
from django.urls import reverse

from lettings.models import Letting, Address


class IndexPageEmptyTest(TestCase):
    def test_index_page_empty_returns_200(self):
        response = self.client.get(reverse("lettings_index"))
        self.assertEqual(response.status_code, 200)

    def test_index_page_empty_uses_correct_template(self):
        response = self.client.get(reverse("lettings_index"))
        self.assertTemplateUsed(response, "lettings/index.html")

    def test_index_page_empty_contains_no_lettings(self):
        response = self.client.get(reverse("lettings_index"))
        self.assertContains(response, "Lettings")
        self.assertContains(response, "No lettings are available.")


class LettingsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.address = Address.objects.create(
            number=123,
            street="Main Street",
            city="Anytown",
            state="NY",
            zip_code=12345,
            country_iso_code="USA",
        )
        cls.letting = Letting.objects.create(title="Test Letting", address=cls.address,)

    def setUp(self):
        self.addressTest = Address.objects.get(id=self.address.id)
        self.lettingTest = Letting.objects.get(id=self.letting.id)

    def test_index_page_contains_lettings_title(self):
        response = self.client.get(reverse("lettings_index"))
        self.assertContains(response, self.lettingTest.title)

    def test_letting_page_returns_200(self):
        response = self.client.get(reverse("letting", args=[self.letting.id]))
        self.assertEqual(response.status_code, 200)

    def test_letting_page_returns_404(self):
        response = self.client.get(reverse("letting", args=[999999]))
        self.assertEqual(response.status_code, 404)

    def test_letting_page_uses_correct_template(self):
        response = self.client.get(reverse("letting", args=[self.letting.id]))
        self.assertTemplateUsed(response, "lettings/letting.html")

    def test_letting_page_contains_letting_data(self):
        response = self.client.get(reverse("letting", args=[self.letting.id]))
        self.assertContains(response, self.lettingTest.title)
        self.assertContains(
            response, str(self.addressTest.number) + " " + self.addressTest.street
        )
        self.assertContains(
            response,
            self.addressTest.city
            + ", "
            + self.addressTest.state
            + " "
            + str(self.addressTest.zip_code),
        )
        self.assertContains(response, self.addressTest.country_iso_code)
