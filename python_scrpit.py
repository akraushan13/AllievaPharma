from app.models import Category, SubCategory, Product
from django.utils.text import slugify

for c in Category.objects.all():
    if not c.slug:
        c.slug = slugify(c.name)
        c.save()

for s in SubCategory.objects.all():
    if not s.slug:
        s.slug = slugify(s.name)
        s.save()