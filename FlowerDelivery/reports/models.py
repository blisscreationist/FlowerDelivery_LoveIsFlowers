# reports/models.py

from django.db import models

class Report(models.Model):
    REPORT_TYPES = [
        ('sales', 'Sales Report'),
        ('popular_products', 'Popular Products Report'),
        ('average_orders', 'Average Orders Report'),
        ('average_ratings', 'Average Ratings Report'),
    ]

    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    date = models.DateField(auto_now_add=True)
    data = models.JSONField()  # Для хранения данных в формате JSON

    def __str__(self):
        return f'{self.get_report_type_display()} - {self.date}'

