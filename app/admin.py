from django.contrib import admin
from .models import Product, ProductImage, Category, SubCategory, JobPosting,JobTag, Application, NewsEvent, NewsEventCategory
# Register your models here.

admin.site.register([Product, ProductImage, Category, SubCategory])
admin.site.register([JobPosting,JobTag])
admin.site.register([Application,])
admin.site.register([NewsEvent, NewsEventCategory])
