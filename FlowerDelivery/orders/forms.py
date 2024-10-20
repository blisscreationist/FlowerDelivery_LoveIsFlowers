# orders/forms.py

from django import forms
from catalog.models import Product
from .models import Order
from django.utils import timezone
from datetime import timedelta
import datetime

class AddToCartForm(forms.Form):
    product_id = forms.IntegerField(widget=forms.HiddenInput)
    quantity = forms.IntegerField(min_value=1, initial=1)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['quantity'].widget.attrs.update({'class': 'form-control'})

DELIVERY_TIME_CHOICES = [(datetime.time(hour, 0), f"{hour:02d}:00") for hour in range(9, 21)]
class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['address', 'telephone', 'delivery_date', 'delivery_time']
        widgets = {
                  'delivery_time': forms.Select(choices=DELIVERY_TIME_CHOICES),
                  }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        today = timezone.now().date()
        self.fields['delivery_date'].widget.attrs.update({
            'min': (today + timedelta(days=1)).isoformat(),
            'max': (today + timedelta(days=8)).isoformat()
        })
