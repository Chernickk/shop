from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from mainapp.models import Product


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def get_order_steps(self):
        steps = self.order_steps.select_related()
        return steps

    def get_order_items(self):
        items = self.orderitems.select_related()
        return items

    def get_current_step(self):
        step = self.order_steps.select_related().order_by('-created_at').first()
        return step

    def get_total_quantity(self):
        items = self.orderitems.select_related()
        return sum(item.quantity for item in items)

    def get_total_cost(self):
        items = self.orderitems.select_related()
        return sum(item.get_total_cost() for item in items)

    def __repr__(self):
        return f'Заказ №{self.id}, пользователя {self.user.username}'


class OrderStep(models.Model):
    FORMING = 'FM'
    SENT_TO_PROCEED = 'STP'
    PROCEEDED = 'PRD'
    PAID = 'PD'
    READY = 'RDY'
    CANCEL = 'CNC'

    ORDER_STATUS_CHOICES = (
        (FORMING, 'формируется'),
        (SENT_TO_PROCEED, 'отправлен в обработку'),
        (PAID, 'оплачен'),
        (PROCEEDED, 'обрабатывается'),
        (READY, 'готов к выдаче'),
        (CANCEL, 'отменен'),
    )

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_steps')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=3, choices=ORDER_STATUS_CHOICES, default=FORMING)

    @receiver(post_save, sender=Order)
    def create(sender, instance, created, **kwargs):
        if created:
            OrderStep.objects.create(order=instance, status=OrderStep.FORMING)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="orderitems", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def get_total_cost(self):
        return self.product.price * self.quantity
