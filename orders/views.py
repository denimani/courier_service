from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from orders.models import DeliveryRequest, DeliveryStatusCurrent
from orders.serializers import DeliveryRequestSerializer
from orders.services import validate_and_correct_address

from geopy import distance

# Координаты складов
WAREHOUSES = {
    'Казань': (55.779363, 49.132366),  # ул. Островского, 98
    'Набережные Челны': (55.744490, 52.430989),  # пр-т. Московский, 161
    'Нижнекамск': (55.637835, 51.818599),  # сквер Лемаева, 2
    'Альметьевск': (54.899379, 52.274017),  # ул. Ленина, 100
    'Зеленодольск': (55.853577, 48.564829),  # ул. Королева, 1
}


class DeliveryRequestViewSet(viewsets.ModelViewSet):
    queryset = DeliveryRequest.objects.all()
    serializer_class = DeliveryRequestSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        city = data.get('city')
        package_type = data.get('package_type')

        # проверка города
        if city not in dict(DeliveryRequest.CITY_CHOICES):
            return Response(
                {"error": "В данном городе не доставляют"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # проверка типа посылки
        if package_type == 'Габаритный груз' and city != 'Казань':
            return Response(
                {"error": "В данном городе не доставляют габаритные посылки"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # валидация и исправления адреса
        address = data.get('address')
        corrected_address, coordinates = validate_and_correct_address(address)
        if not corrected_address:
            return Response(
                {"error": "Не удалось валидировать адрес"},
                status=status.HTTP_400_BAD_REQUEST
            )
        data['address'] = corrected_address

        # расчет расстояния до склада
        warehouse_coords = WAREHOUSES.get(city)
        if not warehouse_coords or not coordinates[0] or not coordinates[1]:
            return Response(
                {"error": "Не удалось определить координаты склада"},
                status=status.HTTP_400_BAD_REQUEST
            )

        distance_km = distance.distance(warehouse_coords, coordinates).km

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(distance=round(distance_km, 2))
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"Заявка": serializer.data['internal_id']},
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    @action(detail=False, methods=['patch'])
    def update_request(self, request, pk):
        delivery_request = self.get_object()
        serializer = self.get_serializer(delivery_request, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"status": "Заявка обновлена"},
            status=status.HTTP_200_OK
        )


class DeliveryRequestStatusView(APIView):
    """
    Получение текущего статуса заявки
    """

    def get(self, request, pk):
        try:
            delivery_status = DeliveryStatusCurrent.objects.get(internal_id=pk)
            return Response(
                {"status": delivery_status.status_name},
                status=status.HTTP_200_OK
            )
        except DeliveryStatusCurrent.DoesNotExist:
            return Response(
                {"error": "Заявка не найдена"},
                status=status.HTTP_404_NOT_FOUND
            )


class UpdateDeliveryRequestStatusView(APIView):
    """
    Обновление статуса заявки на "Done"
    """

    def patch(self, request, pk):
        try:
            delivery_status = DeliveryStatusCurrent.objects.get(internal_id=pk)

            if delivery_status.status_name == 'Done':
                return Response(
                    {"error": "Заявка уже завершена"},
                    status=status.HTTP_200_OK
                )
            else:
                delivery_status.status_name = 'Done'
                delivery_status.save()
                return Response(
                    {"status": "Статус заявки завершен"},
                    status=status.HTTP_200_OK
                )
        except DeliveryStatusCurrent.DoesNotExist:
            return Response(
                {"error": "Заявка не найдена"},
                status=status.HTTP_404_NOT_FOUND
            )
