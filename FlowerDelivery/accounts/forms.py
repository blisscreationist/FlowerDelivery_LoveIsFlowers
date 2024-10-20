# accounts/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email']


class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'telegram_id', 'avatar', 'email']  # Включаем username и email, avatar

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        if 'password1' in self.fields:
            self.fields['password1'].help_text = None
        if 'password2' in self.fields:
            self.fields['password2'].help_text = None

        # Еmail является обязательным полем
        self.fields['email'].required = True
