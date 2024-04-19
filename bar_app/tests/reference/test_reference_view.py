from django.test import TestCase
from rest_framework import status
from bar_app.models import Reference
from bar_app.tests.db_fixture import DbFixture

class ReferencesViewTestCase(DbFixture, TestCase):
    def test_list_references(self):
        response = self.client.get("/api/references/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 5)
        self.assertEqual(response.data["results"][0]["name"], "name 1")
        self.assertEqual(response.data["results"][1]["name"], "name 2")
        self.assertEqual(response.data["results"][2]["name"], "name 3")
        self.assertEqual(response.data["results"][3]["name"], "name 4")
        self.assertEqual(response.data["results"][4]["name"], "name 5")

    def test_filter_references_by_bar_id(self):
        response = self.client.get(f"/api/references/?bar_id={self.bar1.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 4)
        self.assertEqual(response.data["results"][0]["name"], "name 1")
        self.assertEqual(response.data["results"][1]["name"], "name 2")
        self.assertEqual(response.data["results"][2]["name"], "name 3")
        self.assertEqual(response.data["results"][3]["name"], "name 4")

    def test_filter_references_by_in_stock_true(self):
        response = self.client.get("/api/references/?in_stock=true")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 4)
        self.assertEqual(response.data["results"][0]["name"], "name 1")
        self.assertEqual(response.data["results"][1]["name"], "name 2")
        self.assertEqual(response.data["results"][2]["name"], "name 3")

    def test_filter_references_by_in_stock_false(self):
        response = self.client.get("/api/references/?in_stock=false")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["name"], "name 4")

    def test_create_reference(self):
        data = {
            "ref": "new reference",
            "name": "name",
            "description": "description"
        }

        response = self.client.post("/api/references/create/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Reference.objects.filter(ref="new reference").exists())
        self.assertEqual(response.data["detail"], "References created successfully.")

    def test_update_reference(self):
        data = {
            "ref": "new ref",
            "name": "new name",
            "description": "new description"
        }
        response = self.client.put(
            f"/api/references/update/{self.reference1.id}", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        ref = Reference.objects.get(id=self.reference1.id)
        self.assertEqual(ref.name, "new name")
        self.assertEqual(ref.description, "new description")
        self.assertEqual(response.data["detail"], "References updated successfully.")

    def test_delete_reference(self):
        response = self.client.delete(f"/api/references/delete/{self.reference1.id}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Reference.objects.filter(ref="REF001").exists())
        self.assertEqual(response.data["detail"], "Reference deleted successfully")
