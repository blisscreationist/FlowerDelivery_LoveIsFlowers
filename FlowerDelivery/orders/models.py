# orders/models.py

from django.conf import settings
from django.db import models
from django.utils import timezone
from catalog.models import Product
from rest_framework.views import APIView
from django.db.models.signals import post_save
from django.dispatch import receiver
from telegram_utils import send_telegram_message


class Order(models.Model):
    STATUS_CHOICES = [
        ('Ordered', 'Оформлен'),
        ('In Progress', 'В работе'),
        ('Delivering', 'Доставляется'),
        ('Completed', 'Завершен'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateField(default=timezone.now)  # Дата доставки
    delivery_time = models.TimeField(default=timezone.now)  # Время доставки
    address = models.CharField(max_length=255)  # Адрес доставки
    contact = models.CharField(max_length=255, default='Контакт не указан')  # Контактная информация email
    telephone = models.CharField(max_length=255, default='Телефон не указан')  # Контакты, телефоны
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Ordered')

    def __str__(self):
        return f"Order {self.id} by {self.user}"


class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} for {self.user}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)


class OrderCreateApi(APIView):
    def post(self, request, *args, **kwargs):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            # Обработка заказа
            return Response({"message": "Order created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@receiver(post_save, sender=Order)
def send_order_status_update(sender, instance, **kwargs):
    if instance.user.telegram_id:
        status_messages = {
            'Ordered': 'Обновлен статус. Ваш заказ №{order_id} оформлен.',
            'In Progress': 'Обновлен статус. Ваш заказ №{order_id} в работе.',
            'Delivering': 'Обновлен статус. Ваш заказ №{order_id} доставляется.',
            'Completed': 'Обновлен статус. Ваш заказ №{order_id} завершен.',
        }
        message = status_messages.get(instance.status, 'Статус вашего заказа №{order_id} обновлен.')
        message = message.format(order_id=instance.id)
        send_telegram_message(instance.user.telegram_id, message)



