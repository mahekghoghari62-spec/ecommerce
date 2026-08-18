"""Download real stock photos and attach them to sample products (matched
by name) — replaces the plain colored placeholder images from seed_products.

    python manage.py update_product_images
"""

import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from crud.models import Product

# name -> search keyword for a matching real photo
IMAGE_KEYWORDS = {
    "Smartphone": "smartphone",
    "Laptop": "laptop",
    "Bluetooth Speaker": "speaker",
    "Smartwatch": "smartwatch",
    "Denim Jacket": "denim-jacket",
    "Running Shoes": "running-shoes",
    "Cotton T-Shirt": "tshirt",
    "Leather Wallet": "wallet",
    "Non-Stick Pan": "frying-pan",
    "LED Table Lamp": "table-lamp",
    "Cotton Bedsheet": "bedsheet",
    "Wall Clock": "wall-clock",
    "Face Wash": "skincare",
    "Lipstick Set": "lipstick",
    "Hair Dryer": "hairdryer",
    "Perfume": "perfume-bottle",
    "Basmati Rice 5kg": "rice",
    "Cooking Oil 1L": "cooking-oil",
    "Green Tea Pack": "green-tea",
    "Almonds 500g": "almonds",
    "Gift Card": "gift-card",
    "Notebook Set": "notebook",
    "Umbrella": "umbrella",
    "Water Bottle": "water-bottle",
}


class Command(BaseCommand):
    help = "Replace placeholder images with real stock photos for sample products."

    def handle(self, *args, **options):
        updated = 0
        failed = 0

        for name, keyword in IMAGE_KEYWORDS.items():
            try:
                product = Product.objects.get(name=name)
            except Product.DoesNotExist:
                continue

            url = f"https://loremflickr.com/500/500/{keyword}"
            try:
                response = requests.get(url, timeout=15)
                response.raise_for_status()
                product.image.save(
                    f"{name.replace(' ', '_').lower()}.jpg",
                    ContentFile(response.content),
                    save=True,
                )
                updated += 1
                self.stdout.write(f"  \u2713 {name}")
            except Exception as e:
                failed += 1
                self.stdout.write(self.style.WARNING(f"  \u2717 {name}: {e}"))

        self.stdout.write(self.style.SUCCESS(f"Updated {updated} products, {failed} failed."))