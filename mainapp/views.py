from django.shortcuts import render
from django.views.generic.list import ListView
from random import choice
from . import models


class IndexView(ListView):
    template_name = 'mainapp/index.html'
    model = models.Product
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Магазин'
        return context


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

        categories = models.ProductCategory.objects.filter(is_deleted=False)
        context['categories'] = categories

        popular_item = choice(models.Product.objects.all())
        context['popular_item'] = popular_item

        context['title'] = 'Магазин'
        context['pk'] = self.kwargs.get('pk')

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.kwargs.get('pk'):
            category = models.ProductCategory.objects.get(pk=self.kwargs.get('pk'))
            return queryset.filter(category=category)

        return queryset


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