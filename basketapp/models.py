from django.db import models
from django.conf import settings
from mainapp.models import Product
from .managers import BasketQuerySet


class Basket(models.Model):
    objects = BasketQuerySet.as_manager()
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='basket')
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    @property
    def total(self):
        return self.quantity * self.product.price

    def save(self, *args, **kwargs):
        if not self.quantity:
            self.delete()
        else:
            if self.pk:
                self.product.quantity -= self.quantity - self.__class__.objects.get(pk=self.pk).quantity
            else:
                self.product.quantity -= self.quantity
            self.product.save()

            super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.product.quantity += self.quantity
        self.product.save()
        super(Basket, self).delete(*args, **kwargs)
