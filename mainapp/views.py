from django.shortcuts import render
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
    if pk:
        product_list = models.Product.objects.filter(category_id=pk)
    else:
        product_list = models.Product.objects.all()
    context = {
        'title': 'Продукты',
        'categories': categories,
        'product_list': product_list,
        'pk': pk,
    }
    return render(request, 'mainapp/products.html', context=context)
