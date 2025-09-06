from django.utils.text import slugify
from app.models import Product  # replace "app" with your app name

for product in Product.objects.all():
    if not product.slug:  # only if slug is empty
        base_slug = slugify(product.name)
        slug = base_slug
        counter = 1
        # ensure uniqueness
        while Product.objects.filter(slug=slug).exclude(id=product.id).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        product.slug = slug
        product.save()