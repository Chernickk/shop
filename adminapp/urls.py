from django.urls import path
from . import views

app_name = 'adminapp'

urlpatterns = [
    path('users/create/', views.UserCreateView.as_view(), name='user_create'),
    path('users/read/', views.UsersListView.as_view(), name='users'),
    path('users/update/<int:pk>/', views.UserEditView.as_view(), name='user_update'),
    path('users/delete/<int:pk>/', views.user_delete, name='user_delete'),
    path('users/activate/<int:pk>/', views.user_activate, name='user_activate'),
    path('users/deactivate/<int:pk>/', views.user_deactivate, name='user_deactivate'),

    path('categories/create/', views.CategoryCreateView.as_view(), name='category_create'),
    path('categories/read/', views.CategoryListView.as_view(), name='categories'),
    path('categories/update/<int:pk>/', views.CategoryEditView.as_view(), name='category_update'),
    path('categories/delete/<int:pk>/', views.category_delete, name='category_delete'),

    path('products/create/', views.ProductCreateView.as_view(), name='product_create'),
    path('products/read/<int:pk>/', views.ProductView.as_view(), name='product'),
    path('products/category/read/<int:pk>/', views.ProductListView.as_view(), name='products_category'),
    path('products/update/<int:pk>/', views.ProductEditView.as_view(), name='product_update'),
    path('products/delete/<int:pk>/', views.product_delete, name='product_delete'),
]
