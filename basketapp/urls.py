from django.urls import path
from . import views

app_name = 'basketapp'

urlpatterns = [
    path('', views.basket, name='basket'),
    path('add_item/<int:pk>/', views.add_item, name='add_item'),
    path('remove_item/<int:pk>/', views.remove_item, name='remove_item'),
]