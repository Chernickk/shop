from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.products, name='products'),
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
]
