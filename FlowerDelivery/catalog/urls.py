# catalog/urls.py

from django.urls import path
from . import views
from .views import product_detail, ProductListView, contact

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<int:category_id>/', views.product_list, name='product_list'),
    path('categories/', views.category_list, name='category_list'),
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('api/products/', ProductListView.as_view(), name='product-list'),
    path('api/products/<int:pk>/', product_detail, name='product_detail'),
    path('api/categories/', views.category_list_api, name='category_list_api'),
    path('contact/', contact, name='contact'),


]



