from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth.models import User
from bar_app.models import Reference, Bar, Stock

class StatisticsViewTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.create_test_data()

    def setUp(self):
        self.user = User.objects.create_user(username="admin", password="admin", is_staff=True)
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    @classmethod
    def create_test_data(cls):
        cls.reference1 = Reference.objects.create(ref="REF001", name="name 1", description="description 1")
        cls.reference2 = Reference.objects.create(ref="REF002", name="name 2", description="description 2")
        cls.reference3 = Reference.objects.create(ref="REF003", name="name 3", description="description 3")
        cls.reference4 = Reference.objects.create(ref="REF004", name="name 4", description="description 4")

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

    def test_statistics_view(self):
        response = self.client.get("/api/stat/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("all_stocks", response.data)
        self.assertIn("miss_at_least_one", response.data)
        all_stocks = response.data["all_stocks"]
        self.assertIn("description", all_stocks)
        self.assertIn("bars", all_stocks)
        self.assertTrue(isinstance(all_stocks["bars"], list))
        self.assertEqual(all_stocks["bars"], [6])
        miss_at_least_one = response.data["miss_at_least_one"]
        self.assertIn("description", miss_at_least_one)
        self.assertIn("bars", miss_at_least_one)
        self.assertTrue(isinstance(miss_at_least_one["bars"], list))
        self.assertEqual(miss_at_least_one["bars"], [7])
