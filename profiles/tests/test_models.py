from django.test import TestCase
from django.contrib.auth.models import User

from profiles.models import Profile


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

    def test_profile_creation(self):
        profile = Profile.objects.get(id=self.profile.user.id)
        self.assertEqual(self.profile.user, profile.user)
        self.assertEqual(self.profile.favorite_city, profile.favorite_city)
        self.assertTrue(isinstance(self.profile, Profile))
        self.assertEqual(self.profile.__str__(), profile.user.username)
