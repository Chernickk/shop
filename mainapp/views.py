from django.shortcuts import render


def index(request):
    context = {
        'title': 'Магазин'
    }
    return render(request, 'mainapp/index.html', context=context)


def contact(request):
    context = {
        'title': 'Контакты'
    }
    return render(request, 'mainapp/contact.html', context=context)


def products(request):
    links_menu = [
        {'href': '#', 'name': 'все'},
        {'href': '#', 'name': 'дом'},
        {'href': '#', 'name': 'офис'},
        {'href': '#', 'name': 'модерн'},
        {'href': '#', 'name': 'классика'}
    ]
    context = {
        'title': 'Продукты',
        'links_menu': links_menu
    }
    return render(request, 'mainapp/products.html', context=context)
