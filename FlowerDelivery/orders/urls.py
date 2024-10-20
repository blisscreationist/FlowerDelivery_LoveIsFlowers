# orders/urls.py

from django.urls import path, include
from .import views
from .views import OrderViewSet, OrderCreateApi, admin_orders_view, change_order_status, OrderStatusApi, UserOrdersApi, \
    repeat_order, order_success, delete_order
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'orders', OrderViewSet)

urlpatterns = [
   # path('create/', views.OrderCreateView.as_view(), name='order_create'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/', views.update_cart, name='update_cart'),
    path('success/', views.order_success, name='order_success'),
    path('create/', views.order_create, name='order_create'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('get_csrf_token/', views.get_csrf_token_view, name='get_csrf_token'),
    path('', include(router.urls)),
    path('api/orders/', OrderCreateApi.as_view(), name='order-create'),
    path('admin/', admin_orders_view, name='admin_orders'),
    path('admin/<int:order_id>/<str:status>/', change_order_status, name='change_order_status'),
    path('admin/delete_order/<int:order_id>/', delete_order, name='delete_order'),
    path('api/order_status/<int:order_id>/', OrderStatusApi.as_view(), name='order_status_api'),
    path('api/user_orders/', UserOrdersApi.as_view(), name='user_orders'),
    path('<int:order_id>/repeat/', repeat_order, name='repeat_order'),
    path('reviews/', include('reviews.urls')),

]




