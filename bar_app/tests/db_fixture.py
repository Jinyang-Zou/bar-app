from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from bar_app.models import Reference, Bar, Stock

class DbFixture(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.create_test_data()

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="admin", password="admin", is_staff=True)
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    @classmethod
    def create_test_data(cls):
        cls.reference1 = Reference.objects.create(
            ref="REF001", name="name 1", description="description 1")
        cls.reference2 = Reference.objects.create(
            ref="REF002", name="name 2", description="description 2")
        cls.reference3 = Reference.objects.create(
            ref="REF003", name="name 3", description="description 3")
        cls.reference4 = Reference.objects.create(
            ref="REF004", name="name 4", description="description 4")
        cls.reference5 = Reference.objects.create(
            ref="REF005", name="name 5", description="description 5")
        cls.reference6 = Reference.objects.create(
            ref="REF006", name="name 6", description="description 6")

        cls.bar1 = Bar.objects.create(name="bar 1")
        cls.bar2 = Bar.objects.create(name="bar 2")

        Stock.objects.create(reference=cls.reference1, bar=cls.bar1, stock=10)
        Stock.objects.create(reference=cls.reference2, bar=cls.bar1, stock=8)
        Stock.objects.create(reference=cls.reference3, bar=cls.bar1, stock=5)
        Stock.objects.create(reference=cls.reference4, bar=cls.bar1, stock=5)

        Stock.objects.create(reference=cls.reference1, bar=cls.bar2, stock=10)
        Stock.objects.create(reference=cls.reference2, bar=cls.bar2, stock=8)
        Stock.objects.create(reference=cls.reference3, bar=cls.bar2, stock=5)
        Stock.objects.create(reference=cls.reference4, bar=cls.bar2, stock=0)
