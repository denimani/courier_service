from django.contrib import admin

from orders.models import DeliveryRequest, DeliveryRequestStatusHistory, DeliveryStatusCurrent

admin.site.register(DeliveryRequest)

admin.site.register(DeliveryRequestStatusHistory)

admin.site.register(DeliveryStatusCurrent)
