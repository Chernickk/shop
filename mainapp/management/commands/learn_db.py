from django.core.management.base import BaseCommand
from datetime import timedelta, datetime
from mainapp.models import Product
from django.db import connection
from django.db.models import Q, F, When, Case
from django.db.models import DecimalField, IntegerField
from adminapp.views import db_profile_by_type
from ordersapp.models import OrderItem, OrderStep


class Command(BaseCommand):
    def handle(self, *args, **options):
        # test_products = Product.objects.filter(
        #     Q(category__name='Офис') |
        #     Q(category__name='Модерн')
        # )
        #
        # [print(product.name, product.category.name) for product in test_products]
        #
        # db_profile_by_type('learn db', '', connection.queries)

        ACTION_1 = 1
        ACTION_2 = 2
        ACTION_EXPIRED = 3

        action_1__time_delta = timedelta(hours=12)
        action_2__time_delta = timedelta(days=1)

        action_1__discount = 0.3
        action_2__discount = 0.15
        action_expired__discount = 0.05

        action_1_steps = OrderStep.objects.filter(Q(created_at__gt=datetime.now() - action_1__time_delta) &
                                                  Q(status=OrderStep.FORMING))
        action_2_steps = OrderStep.objects.filter(Q(created_at__lte=datetime.now() - action_1__time_delta) &
                                                  Q(created_at__gte=datetime.now() - action_2__time_delta) &
                                                  Q(status=OrderStep.FORMING))
        action_3_steps = OrderStep.objects.filter(Q(created_at__lt=datetime.now() - action_2__time_delta) &
                                                  Q(status=OrderStep.FORMING))

        action_1_orders = [step.order for step in action_1_steps]
        action_2_orders = [step.order for step in action_2_steps]
        action_3_orders = [step.order for step in action_3_steps]

        action_1__condition = Q(order__in=action_1_orders)
        action_2__condition = Q(order__in=action_2_orders)
        action_expired__condition = Q(order__in=action_3_orders)

        action_1__order = When(action_1__condition, then=ACTION_1)
        action_2__order = When(action_2__condition, then=ACTION_2)
        action_expired__order = When(action_expired__condition, then=ACTION_EXPIRED)

        action_1__price = When(action_1__condition, then=F('product__price') * F('quantity') * (1 - action_1__discount))

        action_2__price = When(action_2__condition, then=F('product__price') * F('quantity') * (1 - action_2__discount))

        action_expired__price = When(action_expired__condition,
                                     then=F('product__price') * F('quantity') * (1 - action_expired__discount))

        test_orders = OrderItem.objects.annotate(
            action_order=Case(
                action_1__order,
                action_2__order,
                action_expired__order,
                output_field=IntegerField(),
            )).annotate(
            total_price=Case(
                action_1__price,
                action_2__price,
                action_expired__price,
                output_field=DecimalField(),
            )).order_by('action_order', 'total_price').select_related()

        for orderitem in test_orders:
            print(f'{orderitem.action_order:^2}: '
                  f' заказ №{orderitem.pk:^3}|'
                  f' {orderitem.product.name:^15}|'
                  f' цена: {orderitem.get_total_cost():^15}|'
                  f' скидка: {abs(orderitem.total_price):^6.2f} руб.')
