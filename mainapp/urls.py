from django.urls import path
from . import views
<<<<<<< HEAD
urlpatterns = [
    path('', views.index),
    path('contact/', views.contact),
    path('products/', views.products)
]
=======

urlpatterns = [
    path('products/', views.products, name='products'),
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
]
>>>>>>> 66aa113d1e148654d977ef291e790a97004349b0
