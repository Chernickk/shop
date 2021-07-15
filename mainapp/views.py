from django.shortcuts import render
from random import choice
from . import models


def index(request):
    product_list = models.Product.objects.all().order_by('-created_at')[:4]
    context = {
        'title': 'Магазин',
        'product_list': product_list,
    }
    return render(request, 'mainapp/index.html', context=context)


def contact(request):
    context = {
        'title': 'Контакты',
    }
    return render(request, 'mainapp/contact.html', context=context)


def products(request, pk=None):
    categories = models.ProductCategory.objects.all()
    if pk is not None:
        product_list = models.Product.objects.filter(category_id=pk).order_by('-created_at')[:3]
    else:
        product_list = models.Product.objects.all().order_by('-created_at')[:3]

    popular_item = choice(models.Product.objects.all())

    context = {
        'title': 'Продукты',
        'categories': categories,
        'product_list': product_list,
        'pk': pk,
        'popular_item': popular_item
    }
    return render(request, 'mainapp/products.html', context=context)


def product(request, pk):
    product_ = models.Product.objects.get(pk=pk)

    context = {
        'title': f'{product_.name}',
        'product': product_
    }

    return render(request, 'mainapp/product.html', context=context)