from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date


class ShopUser(AbstractUser):
    image = models.ImageField()
    date_of_birth = models.DateField(null=True)
    is_deleted = models.BooleanField(default=False)

    @property
    def age(self):
        if self.date_of_birth:
            delta = date.today().year - self.date_of_birth.year
            if date.today().month > self.date_of_birth.month or \
                    (date.today().month == self.date_of_birth.month and date.today().day >= self.date_of_birth.day):
                return delta
            return delta - 1
