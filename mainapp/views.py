from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic.list import ListView
from django.conf import settings
from django.core.cache import cache
from random import choice
from . import models


# Cache functions

def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = models.ProductCategory.objects.filter(is_deleted=False)
            cache.set(key, links_menu)
    else:
        links_menu = models.ProductCategory.objects.filter(is_deleted=False)

    return links_menu


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category = cache.get(key)
        if category is None:
            category = models.ProductCategory.objects.get(pk=pk)
            cache.set(key, category)
    else:
        category = models.ProductCategory.objects.get(pk=pk)

    return category


def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = models.Product.get_items()
            cache.set(key, products)
    else:
        products = models.Product.get_items()

    return products


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product_{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(models.Product, pk=pk, is_deleted=False)
            cache.set(key, product)
    else:
        product = get_object_or_404(models.Product, pk=pk, is_deleted=False)

    return product


def get_popular_product():
    if settings.LOW_CACHE:
        key = f'popular_product'
        product = cache.get(key)
        if product is None:
            product = choice(get_products())
            cache.set(key, product)
    else:
        product = choice(get_products())

    return product


def get_products_ordered_by_price():
    if settings.LOW_CACHE:
        key = 'products_ordered_by_price'
        products = cache.get(key)
        if products is None:
            products = models.Product.objects.filter(is_deleted=False).order_by('price')
            cache.set(key, products)
    else:
        products = models.Product.objects.filter(is_deleted=False).order_by('price')

    return products


def get_products_from_category_ordered_by_price(pk):
    if settings.LOW_CACHE:
        key = f'products_from_category_{pk}_ordered_by_price'
        products = cache.get(key)
        if products is None:
            products = models.Product.objects.filter(is_deleted=False, category__pk=pk).order_by('price')
            cache.set(key, products)
    else:
        products = models.Product.objects.filter(is_deleted=False, category__pk=pk).order_by('price')

    return products


# Views

class IndexView(ListView):
    template_name = 'mainapp/index.html'
    model = models.Product
    ordering = 'created_at'
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Магазин'
        return context

    def get_queryset(self):
        return get_products()


def contact(request):
    context = {
        'title': 'Контакты',
    }
    return render(request, 'mainapp/contact.html', context=context)


class ProductsView(ListView):
    template_name = 'mainapp/products.html'
    model = models.Product
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        categories = get_links_menu()
        context['categories'] = categories

        popular_item = get_popular_product()
        context['popular_item'] = popular_item

        context['title'] = 'Магазин'
        context['pk'] = self.kwargs.get('pk')

        return context

    def get_queryset(self):
        queryset = get_products()
        if self.kwargs.get('pk'):
            category = models.ProductCategory.objects.get(pk=self.kwargs.get('pk'))
            return queryset.filter(category=category)

        return queryset


def product(request, pk):
    product_ = get_product(pk)

    context = {
        'title': f'{product_.name}',
        'product': product_
    }

    return render(request, 'mainapp/product.html', context=context)


def products_ajax(request, category_pk=None, page=1):
    if request.is_ajax():
        links_menu = get_links_menu()
        if category_pk is not None:
            if category_pk == '0':
                products = get_products_ordered_by_price()
                category_name = 'все'
            else:
                category_name = get_category(category_pk).name
                products = get_products_from_category_ordered_by_price(pk=category_pk)

            paginator = Paginator(products, 2)
            try:
                products_paginator = paginator.page(page)
            except PageNotAnInteger:
                products_paginator = paginator.page(1)
            except EmptyPage:
                products_paginator = paginator.page(paginator.num_pages)

            context = {
                'links_menu': links_menu,
                'category': category_name,
                'category_pk': category_pk,
                'products': products_paginator,
            }

            result = render_to_string(
                'includes/_product_list_content.html',
                context=context,
                request=request
            )

            return JsonResponse({'result': result})

