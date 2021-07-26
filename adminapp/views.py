from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic.list import ListView
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from authapp.models import ShopUser
from mainapp.models import Product
from mainapp.models import ProductCategory
from . import forms


class UserCreateView(CreateView):
    template_name = 'adminapp/user_create.html'
    model = ShopUser
    success_url = reverse_lazy('shopadmin:users')
    form_class = forms.ShopUserAdminRegisterForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Админка.пользователи'
        return context


class UsersListView(ListView):
    template_name = 'adminapp/users.html'
    model = ShopUser
    ordering = ('-is_active', '-is_superuser', '-is_staff', 'username')
    paginate_by = 5

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Админка.пользователи.создание'
        return context


class UserEditView(UpdateView):
    template_name = 'adminapp/user_update.html'
    model = ShopUser
    success_url = reverse_lazy('shopadmin:users')
    form_class = forms.ShopUserAdminEditProfileForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Админка.пользователи.редактирование'
        return context


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


class CategoryCreateView(CreateView):
    template_name = 'adminapp/category_create.html'
    model = ProductCategory
    success_url = reverse_lazy('shopadmin:categories')
    form_class = forms.CategoryCreateForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Админка.категории.создание'
        return context


class CategoryListView(ListView):
    template_name = 'adminapp/categories.html'
    model = ProductCategory

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Админка.категории'
        return context


class CategoryEditView(UpdateView):
    template_name = 'adminapp/category_update.html'
    model = ProductCategory
    success_url = reverse_lazy('shopadmin:categories')
    form_class = forms.CategoryEditForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Админка.категории.редактирование'
        return context


@user_passes_test(lambda u: u.is_superuser)
def category_delete(request, pk):
    category = ProductCategory.objects.get(pk=pk)
    category.is_deleted = True
    category.save()

    return redirect(request.META.get('HTTP_REFERER', '/'))


class ProductCreateView(CreateView):
    template_name = 'adminapp/product_create.html'
    model = Product
    success_url = reverse_lazy('shopadmin:categories')
    form_class = forms.ProductCreateForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Админка.продукты.создание'
        return context


class ProductView(DetailView):
    model = Product
    template_name = 'adminapp/product_read.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Админка.продукт'
        return context


class ProductListView(ListView):
    template_name = 'adminapp/products.html'
    model = Product
    ordering = ('name', 'created_at')
    paginate_by = 10

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Админка.продукты'
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(category__id=self.kwargs['pk'])


class ProductEditView(UpdateView):
    template_name = 'adminapp/product_update.html'
    model = Product
    success_url = reverse_lazy('shopadmin:product')
    form_class = forms.ProductEditForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Админка.продукт.редактирование'
        return context


@user_passes_test(lambda u: u.is_staff)
def product_delete(request, pk):
    product = Product.objects.get(pk=pk)
    product.is_deleted = True
    product.save()

    return redirect(request.META.get('HTTP_REFERER', '/'))

