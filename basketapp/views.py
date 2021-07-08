from django.shortcuts import render
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from mainapp.models import Product
from .models import Basket


def basket(request):
    if request.user.is_authenticated:
        user = request.user
        basket_list = Basket.objects.filter(user=user)
        total_sum = sum(item.total for item in basket_list)
        total_count = sum(item.quantity for item in basket_list)

    context = {
        'title': 'Корзина',
        'basket_list': basket_list,
        'total_sum': total_sum,
        'total_count': total_count,
    }

    return render(request, 'basketapp/basket.html', context=context)


def add_item(request, pk):
    product = Product.objects.get(pk=pk)
    basket, created = Basket.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        if product.quantity > basket.quantity:
            basket.quantity += 1
            basket.save()

    return redirect(request.META.get('HTTP_REFERER'))


def remove_item(request, pk):
    product = Product.objects.get(pk=pk)
    try:
        basket = Basket.objects.get(
            user=request.user,
            product=product
        )

        if basket.quantity == 1:
            basket.delete()
        else:
            basket.quantity -= 1
            basket.save()

    except ObjectDoesNotExist as e:
        pass

    return redirect(request.META.get('HTTP_REFERER'))

