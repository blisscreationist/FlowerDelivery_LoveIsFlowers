# accounts/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.decorators import login_required
from .views import check_user_exists, CheckUserExistsByTelegramId
from .views import SignUpView, profile

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('profile/', profile, name='profile'),  # Маршрут для профиля
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'),
         name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),
    path('password_change/', login_required(auth_views.PasswordChangeView.as_view()), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('api/check_user_exists/', check_user_exists, name='check_user_exists'),
    path('api/check_user_exists_tg/', CheckUserExistsByTelegramId.as_view(), name='check_user_exists_tg'),
    path('api/register/', views.register_via_telegram, name='register_via_telegram'),
]
