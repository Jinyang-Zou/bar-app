from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from bar_app.models import Reference, Bar, Stock

class ReferencesViewTestCase(TestCase):
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

        cls.bar1 = Bar.objects.create(name="bar 1")
        cls.bar2 = Bar.objects.create(name="bar 2")

        Stock.objects.create(reference=cls.reference1, bar=cls.bar1, stock=10)
        Stock.objects.create(reference=cls.reference2, bar=cls.bar1, stock=8)
        Stock.objects.create(reference=cls.reference3, bar=cls.bar1, stock=5)
        Stock.objects.create(reference=cls.reference4, bar=cls.bar1, stock=0)

        Stock.objects.create(reference=cls.reference1, bar=cls.bar2, stock=10)
        Stock.objects.create(reference=cls.reference2, bar=cls.bar2, stock=8)
        Stock.objects.create(reference=cls.reference3, bar=cls.bar2, stock=5)
        Stock.objects.create(reference=cls.reference4, bar=cls.bar2, stock=0)

    def test_list_references(self):
        response = self.client.get("/api/references/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 4)
        self.assertEqual(response.data["results"][0]["name"], "name 1")
        self.assertEqual(response.data["results"][1]["name"], "name 2")
        self.assertEqual(response.data["results"][2]["name"], "name 3")
        self.assertEqual(response.data["results"][3]["name"], "name 4")

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
        self.assertEqual(len(response.data["results"]), 3)
        self.assertEqual(response.data["results"][0]["name"], "name 1")
        self.assertEqual(response.data["results"][1]["name"], "name 2")
        self.assertEqual(response.data["results"][2]["name"], "name 3")

    def test_filter_references_by_in_stock_false(self):
        response = self.client.get("/api/references/?in_stock=false")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["name"], "name 4")

    def test_unknown_query_param(self):
        response = self.client.get("/api/references/?unknown_param=1")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "Unknown parameter: unknown_param.")

    def test_create_reference(self):
        data = {
            "ref": "REF005",
            "name": "name",
            "description": "description"
        }

        response = self.client.post("/api/references/create/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Reference.objects.filter(ref="REF005").exists())
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
