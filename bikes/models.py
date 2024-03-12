from django.db import models
from django.utils import timezone

def set_this_attribute(data, key, self):
    if not data.__dict__[key]:
        return True

class Bikes(models.Model):
    actual = models.DecimalField(max_digits=5, decimal_places=1, null=True)
    forecast = models.DecimalField(max_digits=20, decimal_places=15, null=True)
    upper = models.DecimalField(max_digits=20, decimal_places=15, null=True)
    lower = models.DecimalField(max_digits=20, decimal_places=15, null=True)
    date_time = models.DateTimeField(unique=True, primary_key=True)

    def __str__(self) -> str:
        return self.date_time.strftime("%Y-%m-%d %H:%M:%S")

    def save_result(self, *args, **kwargs):
        requires_save = False
        bikes_data, is_created = Bikes.objects.update_or_create(
            date_time=self.date_time,
        )
        requires_save = is_created
        if set_this_attribute(bikes_data, "actual", self):
            requires_save = True
            setattr(bikes_data, "actual", self.actual)
        if set_this_attribute(bikes_data, "forecast", self):
            setattr(bikes_data, "forecast", self.forecast)
        if set_this_attribute(bikes_data, "upper", self):
            setattr(bikes_data, "upper", self.upper)
        if set_this_attribute(bikes_data, "lower", self):
            setattr(bikes_data, "lower", self.lower)
        if requires_save:
            bikes_data.save()

    @classmethod
    def create(cls, date_time):
        bikes = cls(date_time=date_time)
        # do something with the book
        return bikes
