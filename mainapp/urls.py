from django.urls import path
from . import views

urlpatterns = [
    path('', views.products, name='index'),
    path('<int:pk>/', views.products, name='products'),
]
