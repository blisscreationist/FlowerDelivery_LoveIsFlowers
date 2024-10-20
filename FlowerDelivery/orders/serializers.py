#orders/serializers.py
from rest_framework import serializers
from .models import Order, OrderItem
from catalog.models import Product

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['user', 'delivery_date', 'delivery_time', 'address', 'contact', 'total_amount', 'status', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')  # Извлекаем вложенные данные
        order = Order.objects.create(**validated_data)  # Создаем заказ
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)  # Создаем связанные элементы заказа
        return order

class OrderListSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)  # Используем вложенный сериализатор для чтения

    class Meta:
        model = Order
        fields = ['id', 'status', 'total_amount', 'delivery_date', 'items']  # Включаем элементы заказа

class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'status']


