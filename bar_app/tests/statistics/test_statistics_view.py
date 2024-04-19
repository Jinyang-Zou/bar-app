from django.test import TestCase
from rest_framework import status
from bar_app.tests.db_fixture import DbFixture

class StatisticsViewTestCase(DbFixture, TestCase):
    def test_statistics_view(self):
        response = self.client.get("/api/stat/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("all_stocks", response.data)
        self.assertIn("miss_at_least_one", response.data)

        all_stocks = response.data["all_stocks"]
        self.assertIn("description", all_stocks)
        self.assertIn("bars", all_stocks)
        self.assertTrue(isinstance(all_stocks["bars"], list))
        self.assertEqual(all_stocks["bars"], [8])

        miss_at_least_one = response.data["miss_at_least_one"]
        self.assertIn("description", miss_at_least_one)
        self.assertIn("bars", miss_at_least_one)
        self.assertTrue(isinstance(miss_at_least_one["bars"], list))
        self.assertEqual(miss_at_least_one["bars"], [9])
