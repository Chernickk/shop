from django.contrib import admin
from . import models


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('category', 'name', 'description', 'image', 'price', 'quantity', 'created_at', 'updated_at')


admin.site.register(models.ProductCategory, ProductCategoryAdmin)
admin.site.register(models.Product, ProductAdmin)


