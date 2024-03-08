from django.db import models
from django.utils import timezone

class Bikes(models.Model):
    actual = models.DecimalField(max_digits=5, decimal_places=1)
    forecast = models.DecimalField(max_digits=20, decimal_places=15)
    upper = models.DecimalField(max_digits=20, decimal_places=15)
    lower = models.DecimalField(max_digits=20, decimal_places=15)
    date_time = models.TextField()

    def __str__(self) -> str:
        return self.date_time

    def save(self, *args, **kwargs):
        try:
            Bikes.objects.get(date_time=self.date_time)
            print(self.date_time, ' already exists.')
        except Bikes.DoesNotExist:
            super().save(*args, **kwargs)

    @classmethod
    def create(cls, date_time):
        bikes = cls(date_time=date_time)
        # do something with the book
        return bikes
