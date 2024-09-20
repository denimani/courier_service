from django.urls import path
from rest_framework import routers

from orders.apps import OrdersConfig
from orders.views import DeliveryRequestViewSet, DeliveryRequestStatusView, UpdateDeliveryRequestStatusView

app_name = OrdersConfig.name

router = routers.DefaultRouter()
router.register(r'orders', DeliveryRequestViewSet, basename='orders')

urlpatterns = [
    path('delivery_status/<int:pk>/', DeliveryRequestStatusView.as_view()),
    path('update_delivery_status/<int:pk>/', UpdateDeliveryRequestStatusView.as_view()),
] + router.urls
