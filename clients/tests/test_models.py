from django.test import TestCase
from django.contrib.auth import get_user_model

from ..models import Client 

User = get_user_model()

class TestClientModel(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.staff = User.objects.create_user(
            username="mylo",
            email="mylo@email.com",
            password="Testpass123"
        )
        cls.staff.is_staff = True 
        cls.staff.save()
    
    def setUp(self):
        self.first_client = Client.objects.create(
            first_name="Mano",
            last_name="Dann",
            telephone_number="45677777",
            email="manodann@email.com",
            address="Lumiere, Dennery"
        )

    def test_string_rep(self):
        self.assertEqual("Mano Dann", str(self.first_client))

    def test_get_absolute_url(self):
        url2 = "/private/clients/1/"
        self.assertEqual(self.first_client.get_absolute_url(), url2)

    def test_get_delete_url(self):
        url2 = "/private/clients/1/delete/"
        self.assertEqual(self.first_client.get_delete_url(), url2)

    def test_get_update_url(self):
        url2 = "/private/clients/1/update/"
        self.assertEqual(self.first_client.get_update_url(), url2)

    def test_get_create_url(self):
        url2 = "/private/clients/create/"
        self.assertEqual(self.first_client.get_create_url(), url2)