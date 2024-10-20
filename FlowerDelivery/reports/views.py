# reports/views.py

import json
from django.shortcuts import render
from decimal import Decimal
from catalog.models import Product
from django.utils.timezone import now
from datetime import timedelta
from django.db.models import Sum, Count, Avg, F
from orders.models import Order, OrderItem
from reports.models import Report
from reviews.models import Review

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return super(DecimalEncoder, self).default(obj)

def sales_report(request):
    end_date = now()
    start_date = end_date - timedelta(days=30)  # Отчет о продажах за 30 дней

    # Данные о продажах
    sales_data = OrderItem.objects.filter(
        order__created_at__range=[start_date, end_date]
    ).values(
        'product__name'
    ).annotate(
        total_quantity=Sum('quantity'),
        total_amount=Sum(F('quantity') * F('price'))
    ).order_by('-total_amount')

    sales_data_json = json.dumps(list(sales_data), cls=DecimalEncoder)

    return render(request, 'reports/sales_report.html', {'sales_data': sales_data})


def get_sales_data(start_date, end_date):
    return {
        'total_sales':
            Order.objects.filter(created_at__range=[start_date, end_date]).aggregate(total_sales=Sum('total_amount'))[
                'total_sales'],
        'order_count': Order.objects.filter(created_at__range=[start_date, end_date]).count(),
    }


def popular_products(request):
    end_date = now()
    start_date = end_date - timedelta(days=30)

    # Данные о продажах
    sales_data = OrderItem.objects.filter(
        order__created_at__range=[start_date, end_date]
    ).values('product__name').annotate(
        total_quantity=Sum('quantity'),
        total_amount=Sum('price')
    ).order_by('-total_quantity')

    return render(request, 'reports/popular_products.html', {'sales_data': sales_data})


def get_popular_products(start_date, end_date):
    items = OrderItem.objects.filter(order__created_at__range=[start_date, end_date]) \
        .values('product') \
        .annotate(total_quantity=Sum('quantity')) \
        .order_by('-total_quantity')

    total_sales = sum(item['total_quantity'] for item in items)
    for item in items:
        item['percentage'] = (item['total_quantity'] / total_sales) * 100 if total_sales > 0 else 0

    return items


def average_ratings(request):
    products = Product.objects.annotate(average_rating=Avg('reviews__rating'))
    return render(request, 'reports/average_ratings.html', {'products': products})


def average_orders(request):
    customer_order_counts = Order.objects.values('user').annotate(order_count=Count('id'))
    total_orders = customer_order_counts.count()
    total_customers = Order.objects.values('user').distinct().count()

    average_orders = total_orders / total_customers if total_customers > 0 else 0

    return render(request, 'reports/average_orders.html', {'average_orders': average_orders})

