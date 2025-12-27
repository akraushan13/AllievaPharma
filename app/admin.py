from django.contrib import admin
from .models import ( Product, ProductImage, Category, SubCategory, JobPosting,JobTag,
                      Application, NewsEvent, NewsEventCategory, ProductCSV)
# Register your models here.

admin.site.register([Product, ProductImage, Category, SubCategory])
admin.site.register([JobPosting,JobTag])
admin.site.register([Application,])
admin.site.register([NewsEvent, NewsEventCategory])


@admin.register(ProductCSV)
class ProductCSVAdmin(admin.ModelAdmin):
    list_display = ("uploaded_at",)

    def has_add_permission(self, request):
        # Allow only ONE CSV record
        return not ProductCSV.objects.exists()