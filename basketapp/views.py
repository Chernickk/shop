from django.shortcuts import render
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse
from mainapp.models import Product
from .models import Basket


@login_required
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
            basket.quantity += 1
            basket.save()

    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def remove_item(request, pk):
    product = Product.objects.get(pk=pk)
    try:
        basket = Basket.objects.get(
            user=request.user,
            product=product
        )
        basket.quantity -= 1
        basket.save()

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
