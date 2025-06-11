from django.contrib import admin
from .models import Product, ProductImage, Category, SubCategory
# Register your models here.

admin.site.register([Product, ProductImage, Category, SubCategory])