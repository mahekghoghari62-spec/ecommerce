from django.core.management.base import BaseCommand
from crud.models import Category

class Command(BaseCommand):
    help = "Seed the fixed Clothes tree for Single Category mode"

    def handle(self, *args, **kwargs):
        clothes, _ = Category.objects.get_or_create(name="Clothes")
        for sub in ["Men", "Women", "Kids"]:
            Category.objects.get_or_create(name=sub, parent=clothes)
        self.stdout.write(self.style.SUCCESS("Clothes category tree seeded."))