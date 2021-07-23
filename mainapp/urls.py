from django.urls import path
from . import views

app_name = 'mainapp'

urlpatterns = [
    path('', views.ProductsView.as_view(), name='index'),
    path('<int:pk>/', views.ProductsView.as_view(), name='products'),
    path('product/<int:pk>/', views.product, name='product'),
]
