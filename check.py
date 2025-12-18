from app.models import Category, SubCategory
from django.utils.text import slugify

# Fix categories
for c in Category.objects.filter(slug=""):
    c.slug = slugify(c.name)
    c.save()

# Fix subcategories
for s in SubCategory.objects.filter(slug=""):
    s.slug = slugify(s.name)
    s.save()

print("Slugs fixed successfully")
