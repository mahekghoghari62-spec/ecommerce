from django.db import migrations
from django.utils.text import slugify

LEGACY_MAP = {
    "electronics": "Electronics",
    "fashion": "Fashion",
    "home": "Home & Kitchen",
    "beauty": "Beauty",
    "grocery": "Grocery",
    "other": "Other",
}

def forwards(apps, schema_editor):
    Product = apps.get_model("crud", "Product")
    Category = apps.get_model("crud", "Category")
    for old_key, cat_name in LEGACY_MAP.items():
        category, created = Category.objects.get_or_create(
            name=cat_name,
            defaults={"slug": slugify(cat_name)},
        )
        Product.objects.filter(legacy_category=old_key).update(category=category)

def backwards(apps, schema_editor):
    pass

class Migration(migrations.Migration):
    dependencies = [
        ("crud", "0027_product_legacy_category_alter_product_category"),
    ]
    operations = [
        migrations.RunPython(forwards, backwards),
    ]