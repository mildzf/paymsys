from django.test import TestCase
from django.contrib.auth import get_user_model

from clients.models import Client 
from accts.models import Account 
from ..models import Transaction

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
        self.account = Account.objects.create(
            owner=self.first_client,
            serial_number="32efod8458hrwrer",
            service_fee='50',

        )
        self.first_transaction = Transaction.objects.create(
            account=self.account,
            amount='35',

        )


    def test_string_rep(self):
        self.assertEqual("1", str(self.first_transaction))

    def test_get_absolute_url(self):
        url2 = "/private/transactions/1/"
        self.assertEqual(self.first_transaction.get_absolute_url(), url2)

    def test_get_create_url(self):
        url2 = "/private/transactions/create/"
        self.assertEqual(self.first_transaction.get_create_url(), url2)

    def test_get_create_url(self):
        url2 = "/private/transactions/1/receipt/"
        self.assertEqual(self.first_transaction.get_receipt(), url2)