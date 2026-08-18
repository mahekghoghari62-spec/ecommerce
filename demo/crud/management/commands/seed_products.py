"""Seed the shop with sample products (all categories) + placeholder images.

Generates a simple colored PNG per product using Pillow (no internet needed).
Skips products that already exist by name — safe to re-run, won't touch or
delete your existing products (avoids ProtectedError from linked
Orders/Pricing/Inventory/Quality/InfluencerCampaign records).

    python manage.py seed_products
"""

import io
import random
from decimal import Decimal

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from PIL import Image, ImageDraw, ImageFont

from crud.models import Product

CATEGORY_COLORS = {
    "electronics": "#4e73df",
    "fashion": "#e83e8c",
    "home": "#1cc88a",
    "beauty": "#f6c23e",
    "grocery": "#e74a3b",
    "other": "#858796",
}

PRODUCTS_BY_CATEGORY = {
    "electronics": ["Smartphone", "Laptop", "Bluetooth Speaker", "Smartwatch"],
    "fashion": ["Denim Jacket", "Running Shoes", "Cotton T-Shirt", "Leather Wallet"],
    "home": ["Non-Stick Pan", "LED Table Lamp", "Cotton Bedsheet", "Wall Clock"],
    "beauty": ["Face Wash", "Lipstick Set", "Hair Dryer", "Perfume"],
    "grocery": ["Basmati Rice 5kg", "Cooking Oil 1L", "Green Tea Pack", "Almonds 500g"],
    "other": ["Gift Card", "Notebook Set", "Umbrella", "Water Bottle"],
}


def make_placeholder_image(text, hex_color):
    img = Image.new("RGB", (500, 500), color=hex_color)
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 36)
    except Exception:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), text, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((500 - w) / 2, (500 - h) / 2), text, fill="white", font=font)

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    return ContentFile(buffer.getvalue(), name=f"{text.replace(' ', '_').lower()}.png")


class Command(BaseCommand):
    help = "Seed crud.Product with ~20 sample products across all categories, with images."

    def handle(self, *args, **options):
        created_count = 0
        skipped_count = 0

        for category_key, names in PRODUCTS_BY_CATEGORY.items():
            color = CATEGORY_COLORS.get(category_key, "#4e73df")
            for name in names:
                if Product.objects.filter(name=name).exists():
                    skipped_count += 1
                    continue

                price = Decimal(random.randrange(200, 50000))
                gst = Decimal(random.choice([0, 5, 12, 18, 28]))

                product = Product(
                    name=name,
                    category=category_key,
                    description=f"Sample {name} in {category_key} category.",
                    price=price,
                    gst_percent=gst,
                    status="active",
                )
                product.image.save(
                    f"{name}.png",
                    make_placeholder_image(name, color),
                    save=False,
                )
                product.save()
                created_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"Created {created_count} new products, skipped {skipped_count} existing."
        ))