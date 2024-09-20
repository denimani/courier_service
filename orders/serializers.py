from rest_framework import serializers

from orders.models import DeliveryRequest, DeliveryRequestStatusHistory


class DeliveryRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryRequest
        fields = '__all__'

#
# class DeliveryStatusCurrentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DeliveryRequestStatusHistory
#         fields = '__all__'
