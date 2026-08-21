# crud/management/commands/seed_categories.py
from django.core.management.base import BaseCommand
from crud.models import Category

class Command(BaseCommand):
    help = "Seed sample category tree"

    def handle(self, *args, **kwargs):
        data = {
            "Men Fashion": {
                "Mens Clothing": ["T-Shirts", "Shirts", "Jeans"],
                "Footwear": ["Shoes", "Sandals"],
            },
            "Women Fashion": {
                "Gowns - Ethnic": ["Anarkali Gowns", "Party Gowns"],
                "Sarees": ["Cotton Sarees", "Silk Sarees"],
                "Kurtis": ["Straight Kurtis", "A-Line Kurtis"],
            },
            "Home & Living": {
                "Home Decor": ["Wall Art", "Vases"],
            },
            "Kids & Toys": {
                "Toys": ["Educational Toys", "Soft Toys"],
            },
        }

        for main_name, subs in data.items():
            main, _ = Category.objects.get_or_create(name=main_name, parent=None)
            for sub_name, leaves in subs.items():
                sub, _ = Category.objects.get_or_create(name=sub_name, parent=main)
                for leaf_name in leaves:
                    Category.objects.get_or_create(name=leaf_name, parent=sub)

        self.stdout.write(self.style.SUCCESS("Categories seeded."))