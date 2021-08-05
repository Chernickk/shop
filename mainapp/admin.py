from django.contrib import admin
from . import models
from authapp.models import ShopUser, ShopUserProfile
from basketapp.models import Basket


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('category', 'name', 'description', 'image', 'price', 'quantity', 'created_at', 'updated_at')


admin.site.register(models.ProductCategory, ProductCategoryAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(ShopUser)
admin.site.register(Basket)
admin.site.register(ShopUserProfile)


