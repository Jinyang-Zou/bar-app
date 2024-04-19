from django.test import TestCase
from bar_app.serializers import StatisticsSerializer
from bar_app.tests.db_fixture import DbFixture

class StatisticsSerializerTestCase(DbFixture, TestCase):
    def test_get_all_stocks(self):
        serializer = StatisticsSerializer()
        data = serializer.get_all_stocks()
        self.assertEqual(
            data["description"], "Liste des comptoirs qui ont toutes les références en stock")
        self.assertIn(self.bar1.id, data["bars"])
        self.assertNotIn(self.bar2.id, data["bars"])

    def test_get_miss_at_least_one(self):
        serializer = StatisticsSerializer()
        data = serializer.get_miss_at_least_one()
        self.assertEqual(
            data["description"], "Liste des comptoirs qui ont au moins une référence épuisée")
        self.assertNotIn(self.bar1.id, data["bars"])
        self.assertIn(self.bar2.id, data["bars"])
