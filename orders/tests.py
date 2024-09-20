import json

from rest_framework import status
from rest_framework.test import APITestCase

from orders.models import DeliveryRequest, DeliveryStatusCurrent


class OrderTestCase(APITestCase):
    def setUp(self):
        self.order = DeliveryRequest.objects.create(
            city="Казань",
            address="ул. Минская, 52",
            delivery_date="2024-11-11",
            delivery_time="20:00:00",
            customer="Иван Иванов",
            package_type="Письмо",
        )
        self.status_current = DeliveryStatusCurrent.objects.create(
            internal_id=self.order,
            status_name="New",
        )

    def test_create_order(self):
        """
        Тест на создание заявки
        """
        data = {
            "city": "Казань",
            "address": "ул. Минская, 52",
            "delivery_date": "2024-11-11",
            "delivery_time": "12:00:00",
            "customer": "Петр Петров",
            "package_type": "Письмо",
        }

        response = self.client.post('/api/orders/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_order(self):
        """
        Тест на обновление заявки
        """
        data = {
            "customer": "Петр Петров",
            "package_type": "Бандероль",
        }

        response = self.client.patch(f'/api/orders/{self.order.internal_id}/', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_status_order(self):
        """
        Тест на получение статуса заявки
        """
        response = self.client.get(f'/api/delivery_status/{self.order.internal_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_status_order(self):
        """
        Тест на закрытие заявки
        """
        response = self.client.patch(f'/api/update_delivery_status/{self.order.internal_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # проверка ошибки при попытке закрыть уже закрытую заявку
        response = self.client.patch(f'/api/update_delivery_status/{self.order.internal_id}/')
        self.assertEqual(response.data, {"error": "Заявка уже завершена"})