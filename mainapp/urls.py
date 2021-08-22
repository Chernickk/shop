from django.urls import path
from django.views.decorators.cache import cache_page
from . import views

app_name = 'mainapp'

urlpatterns = [
    path('', views.ProductsView.as_view(), name='index'),
    path('<int:pk>/', views.ProductsView.as_view(), name='products'),
    path('product/<int:pk>/', views.product, name='product'),
    path('contact/', cache_page(3600)(views.contact), name='contact'),
    path('<int:category_pk>/ajax/', views.products_ajax, name='products_ajax'),
    path('<int:category_pk>/page=<int:page>/ajax/', views.products_ajax, name='products_ajax_page'),
]
