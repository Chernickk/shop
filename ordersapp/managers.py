from django.db import models


class OrderItemQuerySet(models.QuerySet):
    def delete(self, *args, **kwargs):
        for item in self:
            item.product.quantity += item.quantity
            item.product.save()
        super(OrderItemQuerySet, self).delete(*args, **kwargs)
