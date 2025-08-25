from django.contrib import admin
from .models import Product, ProductImage, Category, SubCategory, JobPosting,JobTag, Application
# Register your models here.

admin.site.register([Product, ProductImage, Category, SubCategory])
admin.site.register([JobPosting,JobTag])
admin.site.register([Application,])