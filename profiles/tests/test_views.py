from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from profiles.models import Profile


class IndexPageEmptyTest(TestCase):
    def test_index_page_empty_returns_200(self):
        response = self.client.get(reverse("profiles_index"))
        self.assertEqual(response.status_code, 200)

    def test_index_page_empty_uses_correct_template(self):
        response = self.client.get(reverse("profiles_index"))
        self.assertTemplateUsed(response, "profiles/index.html")

    def test_index_page_empty_contains_no_profiles(self):
        response = self.client.get(reverse("profiles_index"))
        self.assertContains(response, "Profiles")
        self.assertContains(response, "No profiles are available.")


class ProfilesTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            username="Someone",
            first_name="LittleName",
            last_name="Name",
            email="someone.name@email.com",
        )
        cls.profile = Profile.objects.create(user=cls.user, favorite_city="Anytown",)

    def setUp(self):
        self.userTest = User.objects.get(id=self.user.id)
        self.profileTest = Profile.objects.get(id=self.profile.id)

    def test_index_page_contains_profiles_username(self):
        response = self.client.get(reverse("profiles_index"))
        self.assertContains(response, self.userTest.username)

    def test_profile_page_returns_200(self):
        response = self.client.get(
            reverse("profile", args=[self.profile.user.username])
        )
        self.assertEqual(response.status_code, 200)

    def test_profile_page_returns_404(self):
        response = self.client.get(reverse("profile", args=["invalid_user"]))
        self.assertEqual(response.status_code, 404)

    def test_profile_page_uses_correct_template(self):
        response = self.client.get(
            reverse("profile", args=[self.profile.user.username])
        )
        self.assertTemplateUsed(response, "profiles/profile.html")

    def test_profile_page_contains_profile_data(self):
        response = self.client.get(
            reverse("profile", args=[self.profile.user.username])
        )
        self.assertContains(response, self.userTest.username)
        self.assertContains(response, "First name: " + self.userTest.first_name)
        self.assertContains(response, "Last name: " + self.userTest.last_name)
        self.assertContains(response, "Email: " + self.userTest.email)
        self.assertContains(
            response, "Favorite city: " + self.profileTest.favorite_city
        )
