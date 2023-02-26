from django.test import TestCase

from lettings.models import Letting, Address

class LettingsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.address = Address.objects.create(
            number = 123,
            street='Main Street',
            city='Anytown',
            state='NY',
            zip_code=12345,
            country_iso_code='USA',
        )
        cls.letting = Letting.objects.create(
            title='Test Letting',
            address=cls.address,
        )

    def test_address_creation(self):
        address = Address.objects.get(id=self.address.id)
        self.assertEqual(self.address.number, address.number)
        self.assertEqual(self.address.street, address.street)
        self.assertEqual(self.address.city, address.city)
        self.assertEqual(self.address.state, address.state)
        self.assertEqual(self.address.zip_code, address.zip_code)
        self.assertEqual(self.address.country_iso_code, address.country_iso_code)
        self.assertTrue(isinstance(self.address, Address))
        self.assertEqual(self.address.__str__(), str(address.number) + ' ' + address.street)

    def test_letting_creation(self):
        letting = Letting.objects.get(id=self.letting.id)
        self.assertTrue(isinstance(self.letting, Letting))
        self.assertEqual(self.letting.title, letting.title)
        self.assertEqual(self.letting.address, letting.address)
        self.assertEqual(self.letting.__str__(), self.letting.title)
