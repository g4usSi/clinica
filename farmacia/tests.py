from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Medicamento


class MedicamentoAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        user_model = get_user_model()
        cls.admin = user_model.objects.create_superuser(
            username="admin_farmacia", password="clave-segura-123"
        )
        cls.user = user_model.objects.create_user(
            username="usuario_farmacia", password="clave-segura-123"
        )

    def setUp(self):
        self.list_url = reverse("medicamentos-list")
        self.data = {
            "name": "Paracetamol 500 mg",
            "description": "Caja de 20 tabletas",
            "stock": 30,
            "price": "12.50",
        }

    def test_jwt_authentication_and_permissions(self):
        self.assertEqual(self.client.get(self.list_url).status_code, status.HTTP_401_UNAUTHORIZED)

        login = self.client.post(
            reverse("login"),
            {"username": "admin_farmacia", "password": "clave-segura-123"},
            format="json",
        )
        self.assertEqual(login.status_code, status.HTTP_200_OK)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {login.data['access']}")
        self.assertEqual(self.client.post(self.list_url, self.data, format="json").status_code,
                         status.HTTP_201_CREATED)

        self.client.force_authenticate(user=self.user)
        self.assertEqual(self.client.get(self.list_url).status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.post(self.list_url, self.data, format="json").status_code,
                         status.HTTP_403_FORBIDDEN)

    def test_admin_can_create_read_update_and_delete(self):
        self.client.force_authenticate(user=self.admin)
        created = self.client.post(self.list_url, self.data, format="json")
        self.assertEqual(created.status_code, status.HTTP_201_CREATED)
        medicine_id = created.data["id"]
        detail_url = reverse("medicamentos-detail", args=[medicine_id])

        detail = self.client.get(detail_url)
        self.assertEqual(detail.status_code, status.HTTP_200_OK)
        self.assertEqual(detail.data["price"], "12.50")

        replacement = {**self.data, "stock": 25, "price": "13.00"}
        self.assertEqual(self.client.put(detail_url, replacement, format="json").status_code,
                         status.HTTP_200_OK)
        patched = self.client.patch(detail_url, {"stock": 20}, format="json")
        self.assertEqual(patched.status_code, status.HTTP_200_OK)
        self.assertEqual(patched.data["stock"], 20)

        self.assertEqual(self.client.delete(detail_url).status_code,
                         status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.client.get(detail_url).status_code,
                         status.HTTP_404_NOT_FOUND)

    def test_rejects_negative_values_and_duplicate_name(self):
        self.client.force_authenticate(user=self.admin)
        for changes in ({"stock": -1}, {"price": "-0.01"}):
            response = self.client.post(self.list_url, {**self.data, **changes}, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(self.client.post(self.list_url, self.data, format="json").status_code,
                         status.HTTP_201_CREATED)
        detail_url = reverse("medicamentos-detail", args=[Medicamento.objects.get().id])
        self.assertEqual(self.client.patch(detail_url, {"stock": -1}, format="json").status_code,
                         status.HTTP_400_BAD_REQUEST)
        duplicate = self.client.post(self.list_url, self.data, format="json")
        self.assertEqual(duplicate.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Medicamento.objects.count(), 1)

    def test_list_can_filter_by_name(self):
        Medicamento.objects.create(name="Paracetamol", stock=10, price="5.00")
        Medicamento.objects.create(name="Ibuprofeno", stock=10, price="6.00")
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.list_url, {"name": "para"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Paracetamol")
