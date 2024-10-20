from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # Определяем поля, которые будут отображаться в списке пользователей
    list_display = ('username', 'email', 'telegram_id', 'first_name', 'last_name', 'is_staff', 'is_active')

    # Поля, по которым можно осуществлять поиск в админке
    search_fields = ('username', 'email', 'telegram_id', 'first_name', 'last_name')

    # Поля, по которым можно фильтровать пользователей
    list_filter = ('is_staff', 'is_active')

    # Поля, которые будут отображаться на странице редактирования пользователя
    fieldsets = UserAdmin.fieldsets

    # Поля, которые будут отображаться при добавлении нового пользователя
    add_fieldsets = UserAdmin.add_fieldsets


# Регистрируем кастомную модель пользователя в админке
admin.site.register(CustomUser, CustomUserAdmin)
from django.contrib import admin

# Register your models here.
