from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test
from authapp.models import ShopUser
from mainapp.models import Product
from mainapp.models import ProductCategory
from .forms import *


@user_passes_test(lambda u: u.is_superuser)
def user_create(request):

    if request.method == 'POST':
        user_form = ShopUserAdminRegisterForm(request.POST, request.FILES)

        if user_form.is_valid():
            user_form.save()
            return redirect('shopadmin:users')

    user_form = ShopUserAdminRegisterForm()

    context = {
        'title': 'Админка.пользователи.создание',
        'form': user_form
    }
    return render(request, 'adminapp/user_create.html', context)


@user_passes_test(lambda u: u.is_superuser)
def users(request):
    users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')

    context = {
        'title': 'Админка.пользователи',
        'users_list': users_list
    }

    return render(request, 'adminapp/users.html', context)


@user_passes_test(lambda u: u.is_superuser)
def user_update(request, pk):
    user = ShopUser.objects.get(pk=pk)

    if request.method == 'POST':
        user_form = ShopUserAdminEditProfileForm(request.POST, request.FILES, instance=user)

        if user_form.is_valid():
            user_form.save()
            return redirect('shopadmin:users')

    user_form = ShopUserAdminEditProfileForm(instance=user)

    context = {
        'title': 'Админка.пользователи.редактирование',
        'form': user_form,
        'user': user
    }
    return render(request, 'adminapp/user_update.html', context)


@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, pk):
    user = ShopUser.objects.get(pk=pk)
    user.is_deleted = True
    user.save()

    return redirect(request.META.get('HTTP_REFERER', '/'))


@user_passes_test(lambda u: u.is_superuser)
def user_activate(request, pk):
    user = ShopUser.objects.get(pk=pk)
    user.is_active = True
    user.save()

    return redirect(request.META.get('HTTP_REFERER', '/'))


@user_passes_test(lambda u: u.is_superuser)
def user_deactivate(request, pk):
    user = ShopUser.objects.get(pk=pk)
    user.is_active = False
    user.save()

    return redirect(request.META.get('HTTP_REFERER', '/'))


@user_passes_test(lambda u: u.is_superuser)
def category_create(request):
    if request.method == 'POST':
        category_form = CategoryCreateForm(data=request.POST)

        if category_form.is_valid():
            category_form.save()
            return redirect('adminapp:categories')

    category_form = CategoryCreateForm()

    context = {
        'title': 'Админка.категории.создание',
        'form': category_form
    }

    return render(request, 'adminapp/category_create.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def categories(request):
    categories_list = ProductCategory.objects.all().order_by('name')

    context = {
        'title': 'Админка.категории',
        'categories_list': categories_list
    }

    return render(request, 'adminapp/categories.html', context)


@user_passes_test(lambda u: u.is_superuser)
def category_update(request, pk):
    category = ProductCategory.objects.get(pk=pk)

    if request.method == 'POST':
        category_form = CategoryEditForm(data=request.POST, instance=category)

        if category_form.is_valid():
            category_form.save()
            return redirect('adminapp:categories')

    category_form = CategoryEditForm(instance=category)

    context = {
        'title': 'Админка.категории.редактирование',
        'form': category_form
    }

    return render(request, 'adminapp/category_update.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def category_delete(request, pk):
    category = ProductCategory.objects.get(pk=pk)
    category.is_deleted = True
    category.save()

    return redirect(request.META.get('HTTP_REFERER', '/'))


@user_passes_test(lambda u: u.is_superuser)
def product_create(request):
    pass


@user_passes_test(lambda u: u.is_staff)
def products(request):
    product_list = Product.objects.all().order_by('created_at', 'name')

    context = {
        'title': 'Админка.пользователи',
        'product_list': product_list
    }

    return render(request, 'adminapp/products.html', context)


@user_passes_test(lambda u: u.is_staff)
def products_category(request, pk):
    category = ProductCategory.objects.get(pk=pk)
    product_list = Product.objects.all().filter(category=category).order_by('name', 'created_at')
    print(product_list)

    context = {
        'title': 'Админка.пользователи',
        'product_list': product_list
    }

    return render(request, 'adminapp/products.html', context)


@user_passes_test(lambda u: u.is_staff)
def product_update(request):
    pass


@user_passes_test(lambda u: u.is_staff)
def product_delete(request):
    pass

