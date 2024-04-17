from django.test import TestCase
from bar_app.models import Reference, Bar, Stock
from bar_app.serializers import ReferenceSerializer

class ReferenceSerializerTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.reference = Reference.objects.create(
            ref="REF001", name="name", description="description"
        )

    def test_serializer_fields(self):
        serializer = ReferenceSerializer(instance=self.reference)
        data = serializer.data
        self.assertEqual(data["ref"], "REF001")
        self.assertEqual(data["name"], "name")
        self.assertEqual(data["description"], "description")

    def test_read_only_id(self):
        serializer = ReferenceSerializer(
            data={"id": 1, "ref": "REF002", "name": "name"}
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
        bar = Bar.objects.create(name="name")
        Stock.objects.create(reference=self.reference, bar=bar, stock=5)
        serializer = ReferenceSerializer(instance=self.reference)
        self.assertEqual(serializer.data["availability"], "available")

        Stock.objects.filter(reference=self.reference).update(stock=0)
        serializer = ReferenceSerializer(instance=self.reference)
        self.assertEqual(serializer.data["availability"], "outofstock")
