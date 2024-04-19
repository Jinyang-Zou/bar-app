from django.test import TestCase
from bar_app.models import Reference, Bar, Stock
from bar_app.serializers import ReferenceSerializer
from bar_app.tests.db_fixture import DbFixture

class ReferenceSerializerTests(DbFixture, TestCase):
    def test_serializer_fields(self):
        serializer = ReferenceSerializer(instance=self.reference1)
        data = serializer.data
        self.assertEqual(data["ref"], "REF001")
        self.assertEqual(data["name"], "name 1")
        self.assertEqual(data["description"], "description 1")

    def test_read_only_id(self):
        serializer = ReferenceSerializer(
            data={"id": 1, "ref": "id read only", "name": "name"}
        )
        self.assertTrue(serializer.is_valid())
        ref = serializer.save()
        self.assertNotEqual(ref.id, 1)

    def test_validate_ref_unique(self):
        serializer = ReferenceSerializer(data={"ref": "REF001", "name": "name"})
        self.assertFalse(serializer.is_valid())
        self.assertIn("ref", serializer.errors)

    def test_validate_name_not_empty(self):
        serializer = ReferenceSerializer(data={"ref": "REF002", "name": " "})
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)

    def test_get_availability(self):
        bar = Bar.objects.create(name="test availability")
        Stock.objects.create(reference=self.reference5, bar=bar, stock=5)
        serializer = ReferenceSerializer(instance=self.reference5)
        self.assertEqual(serializer.data["availability"], "available")

        Stock.objects.filter(reference=self.reference6)
        serializer = ReferenceSerializer(instance=self.reference6)
        self.assertEqual(serializer.data["availability"], "outofstock")
