# reports/urls.py

from django.urls import path
from .views import sales_report, popular_products, average_orders, average_ratings

urlpatterns = [
    path('sales-report/', sales_report, name='sales_report'),
    path('popular-products/', popular_products, name='popular_products'),
    path('average-orders/', average_orders, name='average_orders'),
    path('average-ratings/', average_ratings, name='average_ratings'),
]
