# orders/views.py

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import Order, CartItem
from django.conf import settings
from catalog.models import Product
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.utils import timezone
from django.views.generic import CreateView
from .forms import OrderForm, AddToCartForm
from .serializers import OrderSerializer, OrderStatusSerializer, OrderListSerializer
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import status
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.contrib.auth.decorators import user_passes_test
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from accounts.models import CustomUser
import logging
import requests


logger = logging.getLogger(__name__)
@login_required
def update_cart(request):
    if request.method == 'POST':
        if 'update' in request.POST:
            for key, value in request.POST.items():
                if key.startswith('quantity_'):
                    item_id = key.split('_')[1]
                    try:
                        cart_item = CartItem.objects.get(id=item_id, user=request.user)
                        cart_item.quantity = int(value)
                        cart_item.save()
                    except CartItem.DoesNotExist:
                        continue
        elif 'remove' in request.POST:
            remove_items = request.POST.getlist('remove_items')
            CartItem.objects.filter(id__in=remove_items, user=request.user).delete()

    return redirect('cart_detail')



@login_required
def add_to_cart(request):
    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():
            product_id = form.cleaned_data['product_id']
            quantity = form.cleaned_data['quantity']
            product = get_object_or_404(Product, id=product_id)


            cart_item, created = CartItem.objects.get_or_create(
                user=request.user,
                product=product,
                defaults={'quantity': quantity}
            )

            if not created:

                cart_item.quantity += quantity
                cart_item.save()

            return redirect('cart_detail')
    return redirect('category_list')


@login_required
def cart_detail(request):
    cart_items = CartItem.objects.filter(user=request.user)
    return render(request, 'orders/cart_detail.html', {'cart_items': cart_items})

def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_list.html', {'orders': orders})


# Функция order_create
@login_required
def order_create(request):
    logger.info('Старт обработки создания заказа')


    cart_items = CartItem.objects.filter(user=request.user)


    if not cart_items.exists():
        return redirect('cart_detail')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():

            order = form.save(commit=False)
            order.user = request.user
            order.created_at = timezone.now()
            order.total_amount = sum(item.quantity * item.product.price for item in cart_items)
            order.save()


            for item in cart_items:
                order.items.create(
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )

            # Очиcтка корзины
            cart_items.delete()

            # Проверка наличия у пользователя заполненного Телеграм ID
            if request.user.telegram_id:
                send_telegram_message(request.user.telegram_id, f'Ваш заказ #{order.id} был успешно создан!')
            else:
                return redirect('order_success')

            return redirect('order_success')  # Страница успеха
    else:
        form = OrderForm()

    return render(request, 'orders/order_create.html', {'form': form, 'cart_items': cart_items})

def order_success(request):
    return render(request, 'orders/order_success.html')

def send_telegram_message(chat_id, text):
    bot_token = 'YOUR_BOT_TOKEN'
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'HTML'
    }
    requests.post(url, json=payload)




def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if not order.total_amount:
        order.total_amount = sum(item.quantity * item.price for item in order.items.all())
        order.save()
    return render(request, 'orders/order_detail.html', {'order': order})

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer



class OrderCreateApi(APIView):
    def post(self, request, *args, **kwargs):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()
            return Response({"message": "Order created successfully", "id": order.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_csrf_token_view(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrftoken': csrf_token})


# Проверка прав администратора
def is_admin(user):
    return user.is_staff


@user_passes_test(is_admin)
def admin_orders_view(request):
    status = request.GET.get('status', '')
    delivery_date = request.GET.get('delivery_date', '')

    orders = Order.objects.all()

    if status:
        orders = orders.filter(status=status)
    if delivery_date:
        orders = orders.filter(delivery_date=delivery_date)

    return render(request, 'orders/admin_orders.html', {'orders': orders})

@user_passes_test(is_admin)
def change_order_status(request, order_id, status):
    order = get_object_or_404(Order, id=order_id)
    order.status = status
    order.save()
    return redirect('admin_orders')

@user_passes_test(is_admin)
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    return redirect('admin_orders')

class OrderStatusApi(APIView):
    def get(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
            serializer = OrderStatusSerializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({'error': 'Заказ не найден'}, status=status.HTTP_404_NOT_FOUND)

class UserOrdersApi(APIView):
    def get(self, request):
        telegram_id = request.query_params.get('telegram_id')
        if not telegram_id:
            return Response({'error': 'telegram_id не указан'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(telegram_id=telegram_id)
            orders = Order.objects.filter(user=user)
            serializer = OrderListSerializer(orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Пользователь с указанным telegram_id не найден'},
                            status=status.HTTP_404_NOT_FOUND)
        except CustomUser.MultipleObjectsReturned:
            return Response({'error': 'Найдено несколько пользователей с указанным telegram_id'},
                            status=status.HTTP_400_BAD_REQUEST)
class OrderListApi(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

@login_required
def repeat_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    for item in order.items.all():
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=item.product,
            defaults={'quantity': item.quantity}
        )
        if not created:
            cart_item.quantity += item.quantity
            cart_item.save()
    return redirect('cart_detail')

