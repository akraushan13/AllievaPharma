import csv
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from app.models import Product  # change app name


def generate_unique_slug(base_slug, model):
    """Generate a unique slug by appending -1, -2, etc."""
    slug = base_slug
    counter = 1
    while model.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1
    return slug


class Command(BaseCommand):
    help = "Safe import/update for Product model (UPSERT without touching duplicates)"

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str, help="Path to the CSV file")

    def handle(self, *args, **kwargs):
        csv_file = kwargs["csv_file"]

        created = 0
        updated = 0
        skipped = 0
        unchanged = 0

        try:
            with open(csv_file, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)

                for row in reader:

                    composition = row.get("COMPOSITION", "").strip()
                    name = row.get("NAME", "").strip()

                    if not composition:
                        skipped += 1
                        self.stdout.write(self.style.ERROR("Skipped → Missing COMPOSITION"))
                        continue

                    if not name:
                        name = composition  # fallback

                    try:
                        product = Product.objects.get(composition=composition)
                        # print(row.get("BRAND_NAME"))
                        print(row.get("SIDE_EFFECT"))

                        # Check if data changed
                        if (
                            product.name == name and
                            product.brand_name == (row.get("BRAND_NAME") or "") and
                            product.form == (row.get("FORM") or "") and
                            product.packing == (row.get("PACKING") or "") and
                            product.descriptions == (row.get("DESCRIPTIONS") or "") and
                            product.uses == (row.get("USES") or "") and
                            product.side_effects == (row.get("SIDE_EFFECT") or "") and
                            product.dosage == (row.get("DOSAGE") or "")
                        ):
                            unchanged += 1
                            continue  # skip duplicate rows

                        # Update ONLY fields (do NOT replace slug)
                        product.name = name
                        product.brand_name = row.get("BRAND_NAME") or ""
                        product.form = row.get("FORM") or ""
                        product.packing = row.get("PACKING") or ""
                        product.descriptions = row.get("DESCRIPTIONS") or ""
                        product.uses = row.get("USES") or ""
                        product.side_effects = row.get("SIDE_EFFECT") or ""
                        product.dosage = row.get("DOSAGE") or ""

                        product.save()
                        updated += 1
                        self.stdout.write(self.style.WARNING(f"UPDATED: {composition}"))

                    except Product.DoesNotExist:
                        # Create new product safely
                        base_slug = slugify(composition)[:240]
                        safe_slug = generate_unique_slug(base_slug, Product)
                        

                        Product.objects.create(
                            composition=composition,
                            name=name,
                            brand_name=row.get("BRAND_NAME") or "",
                            form=row.get("FORM") or "",
                            packing=row.get("PACKING") or "",
                            descriptions=row.get("DESCRIPTIONS") or "",
                            uses=row.get("USES") or "",
                            side_effects=row.get("SIDE_EFFECT") or "",
                            dosage=row.get("DOSAGE") or "",
                            slug=safe_slug,
                        )

                        created += 1
                        self.stdout.write(self.style.SUCCESS(f"CREATED: {composition}"))

                # Summary
                self.stdout.write(self.style.SUCCESS("\nImport Completed!"))
                self.stdout.write(self.style.SUCCESS(f"Created: {created}"))
                self.stdout.write(self.style.SUCCESS(f"Updated: {updated}"))
                self.stdout.write(self.style.WARNING(f"Unchanged (duplicate rows): {unchanged}"))
                self.stdout.write(self.style.ERROR(f"Skipped (invalid rows): {skipped}"))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File not found: {csv_file}"))
