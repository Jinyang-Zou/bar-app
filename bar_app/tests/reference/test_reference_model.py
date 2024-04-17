from django.test import TestCase
from bar_app.models import Reference

class ReferenceModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Reference.objects.create(ref="REF001", name="name 1", description="description 1")
        Reference.objects.create(ref="REF002", name="name 2")

    def test_ref_label(self):
        reference = Reference.objects.get(id=1)
        field_label = reference._meta.get_field("ref").verbose_name
        self.assertEqual(field_label, "ref")

    def test_ref_max_length(self):
        reference = Reference.objects.get(id=1)
        max_length = reference._meta.get_field("ref").max_length
        self.assertEqual(max_length, 100)

    def test_ref_unique(self):
        with self.assertRaises(Exception):
            Reference.objects.create(ref="REF001", name="name", description="description")

    def test_ref_blank(self):
        with self.assertRaises(Exception):
            Reference.objects.create(ref=None, name="name", description="description")

    def test_ref_null(self):
        with self.assertRaises(Exception):
            reference = Reference.objects.create(ref=None, name="name", description="description")

    def test_name_label(self):
        reference = Reference.objects.get(id=1)
        field_label = reference._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "name")

    def test_name_max_length(self):
        reference = Reference.objects.get(id=1)
        max_length = reference._meta.get_field("name").max_length
        self.assertEqual(max_length, 100)

    def test_name_blank(self):
        with self.assertRaises(Exception):
            Reference.objects.create(ref="ref", name=None, description="description")

    def test_name_null(self):
        with self.assertRaises(Exception):
            Reference.objects.create(ref="ref", name=None, description="description")

    def test_description_label(self):
        reference = Reference.objects.get(id=1)
        field_label = reference._meta.get_field("description").verbose_name
        self.assertEqual(field_label, "description")

    def test_description_blank(self):
        reference = Reference.objects.create(ref="ref", name="name", description="")
        self.assertEqual(reference.description, "")

    def test_description_null(self):
        reference = Reference.objects.create(ref="ref", name="name", description=None)
        self.assertIsNone(reference.description)

    def test_ordered_references_by_id(self):
        reference = Reference.objects.all()
        expected_order = [1, 2]

        for i, obj in enumerate(reference):
            self.assertEqual(obj.id, expected_order[i])

    def test_object_name_is_name(self):
        reference = Reference.objects.get(id=1)
        expected_object_name = f"{reference.name}"
        self.assertEqual(expected_object_name, str(reference))

    def test_verbose_name(self):
        verbose_name_plural = Reference._meta.verbose_name
        self.assertEqual(verbose_name_plural, "Reference")

    def test_verbose_name_plural(self):
        verbose_name_plural = Reference._meta.verbose_name_plural
        self.assertEqual(verbose_name_plural, "References")
