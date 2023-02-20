from rest_framework import serializers

from .models import PaymentOrder

class OrderSerializer(serializers.ModelSerializer):
    order_date = serializers.DateTimeField(format="%d %B %Y %I:%M %p")

    class Meta:
        model = PaymentOrder
        fields = '__all__'
        depth = 2