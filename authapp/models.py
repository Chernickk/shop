from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class ShopUser(AbstractUser):
    image = models.ImageField()
    date_of_birth = models.DateField(null=True)

    @property
    def age(self):
        delta = timezone.now() - self.date_of_birth
        return delta.years
