from django.core.management.base import BaseCommand
from django.utils.text import slugify
from app.models import Product


class Command(BaseCommand):
    help = "Generate unique slugs for products that don't have one"

    def handle(self, *args, **kwargs):
        updated_count = 0

        for product in Product.objects.all():
            if not product.slug:  # only process empty slugs
                base_slug = slugify(product.name)
                slug = base_slug
                counter = 1

                # Ensure uniqueness
                while Product.objects.filter(slug=slug).exclude(id=product.id).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1

                product.slug = slug
                product.save()
                updated_count += 1
                self.stdout.write(self.style.SUCCESS(f"Generated slug for: {product.name} → {product.slug}"))

        if updated_count == 0:
            self.stdout.write(self.style.WARNING("No products needed slug updates."))
        else:
            self.stdout.write(self.style.SUCCESS(f"✅ Done! {updated_count} products updated."))
