from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from datetime import date, timedelta
from django.utils import timezone


class ShopUser(AbstractUser):
    image = models.ImageField()
    date_of_birth = models.DateField(null=True)
    is_deleted = models.BooleanField(default=False)

    activation_key = models.CharField(max_length=128, null=True)
    activation_key_start_time = models.DateTimeField(default=timezone.now)

    def is_activation_key_valid(self):
        if timezone.now() - timedelta(hours=48) < self.activation_key_start_time:
            return True
        return False

    @property
    def age(self):
        if self.date_of_birth:
            delta = date.today().year - self.date_of_birth.year
            if date.today().month > self.date_of_birth.month or \
                    (date.today().month == self.date_of_birth.month and date.today().day >= self.date_of_birth.day):
                return delta
            return delta - 1


class ShopUserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'F'

    GENDER_CHOICES = (
        (MALE, 'М'),
        (FEMALE, 'Ж'),
    )

    user = models.OneToOneField(ShopUser, unique=True, null=False, db_index=True, on_delete=models.CASCADE)
    tagline = models.CharField(max_length=128, blank=True)
    about = models.TextField(max_length=1024, blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=1, blank=True)

    @receiver(post_save, sender=ShopUser)
    def create(sender, instance, created, **kwargs):
        if created:
            ShopUserProfile.objects.create(user=instance)

    @receiver(post_save, sender=ShopUser)
    def save_profile(sender, instance, **kwargs):
        instance.shopuserprofile.save()

