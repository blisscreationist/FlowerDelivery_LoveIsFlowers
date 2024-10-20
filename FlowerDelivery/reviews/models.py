# reviews/models.py

from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from catalog.models import Product

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    review_text = models.TextField()
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    def __str__(self):
        return f'Review for {self.product.name} by {self.user.username}'
