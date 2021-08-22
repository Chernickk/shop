from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from django.db.models import F

from mainapp.models import Product
from .models import Basket


class BasketListView(ListView):
    template_name = 'basketapp/basket.html'
    model = Basket

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        basket_list = self.get_queryset()
        context['title'] = 'Админка.пользователи.создание'
        context['total_sum'] = sum(item.total for item in basket_list)
        context['total_count'] = sum(item.quantity for item in basket_list)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.filter(user=self.request.user)


@login_required
def add_item(request, pk):
    if 'login' in request.META.get('HTTP_REFERER'):
        return redirect('mainapp:product', pk=pk)

    product = Product.objects.get(pk=pk)
    basket, created = Basket.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        if product.quantity > basket.quantity:
            basket.quantity = F('quantity') + 1

    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def remove_item(request, pk):
    product = Product.objects.get(pk=pk)
    try:
        basket = Basket.objects.get(
            user=request.user,
            product=product
        )
        basket.delete()

    except ObjectDoesNotExist as e:
        pass

    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_edit(request, pk, quantity):
    if request.is_ajax():
        quantity = int(quantity)
        basket_item = Basket.objects.get(pk=int(pk))

        if quantity > 0:
            basket_item.quantity = quantity
            basket_item.save()
        else:
            basket_item.delete()

        basket_list = Basket.objects.filter(user=request.user)
        total_sum = sum(item.total for item in basket_list)
        total_count = sum(item.quantity for item in basket_list)

        context = {
            'basket_list': basket_list,
            'total_sum': total_sum,
            'total_count': total_count,
        }

        result = render_to_string('includes/_basket_list.html', context)

    return JsonResponse({'result': result})
