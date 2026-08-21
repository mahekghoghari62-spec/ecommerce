from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from shop.models import CustomerProfile, SupplierProfile

from .forms import PanelUserForm, ProductForm
from .models import Category, Company, Contact, PanelUser, Product, Project, Tag, Task


class CrudFlowTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user("tester", password="pw", is_staff=True)

    def setUp(self):
        self.client.force_login(self.user)

    def test_list_requires_login(self):
        self.client.logout()
        resp = self.client.get(reverse("crud:contact_list"))
        self.assertEqual(resp.status_code, 302)  # LoginRequiredMixin -> redirect

    def test_panel_user_role_user_can_login_to_shop(self):
        form = PanelUserForm(data={
            "full_name": "Shop Customer",
            "username": "shopcustomer",
            "email": "shop@example.com",
            "password": "pw-12345!",
            "role": "user",
            "phone": "9876543210",
            "status": "active",
        })

        self.assertTrue(form.is_valid(), form.errors)
        panel_user = form.save()

        self.assertFalse(panel_user.user.is_staff)
        self.assertTrue(CustomerProfile.objects.filter(user=panel_user.user).exists())
        self.client.logout()
        self.assertEqual(
            self.client.post(
                reverse("shop:login"),
                {"username": "shopcustomer", "password": "pw-12345!"},
            ).status_code,
            302,
        )

    def test_list_renders_adminlte_themed_table(self):
        Contact.objects.create(name="Ada Lovelace", email="ada@example.com", role="admin", status="active")
        resp = self.client.get(reverse("crud:contact_list"))
        self.assertEqual(resp.status_code, 200)
        html = resp.content.decode()
        self.assertIn('class="card"', html)              # AdminLTE table card wrapper
        self.assertIn("table table-striped", html)       # classes from Table.Meta.attrs
        self.assertIn("Ada Lovelace", html)
        self.assertIn("badge text-bg-success", html)     # status badge column

    def test_create_flashes_message(self):
        resp = self.client.post(
            reverse("crud:contact_create"),
            {"name": "Grace", "email": "grace@example.com", "role": "editor", "status": "pending"},
            follow=True,
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(Contact.objects.filter(name="Grace").exists())
        html = resp.content.decode()
        self.assertIn("alert-success", html)             # messages -> AdminLTE alert
        self.assertIn("created", html)

    def test_form_page_renders_crispy(self):
        html = self.client.get(reverse("crud:contact_create")).content.decode()
        self.assertIn('id="id_name"', html)         # field rendered
        self.assertIn("form-control", html)         # Bootstrap-5 widget classes (crispy)
        self.assertIn('name="save"', html)          # crispy Submit button
        self.assertIn("csrfmiddlewaretoken", html)  # crispy emits the <form> + csrf

    def test_filter_by_status(self):
        Contact.objects.create(name="Alpha", email="a@e.com", status="active")
        Contact.objects.create(name="Bravo", email="b@e.com", status="disabled")
        html = self.client.get(reverse("crud:contact_list"), {"status": "disabled"}).content.decode()
        self.assertIn("Bravo", html)
        self.assertNotIn("Alpha", html)

    def test_update_and_delete(self):
        c = Contact.objects.create(name="Temp", email="t@e.com")
        self.client.post(
            reverse("crud:contact_update", args=[c.pk]),
            {"name": "Renamed", "email": "t@e.com", "role": "viewer", "status": "active"},
        )
        c.refresh_from_db()
        self.assertEqual(c.name, "Renamed")
        self.client.post(reverse("crud:contact_delete", args=[c.pk]))
        self.assertFalse(Contact.objects.filter(pk=c.pk).exists())

    def test_supplier_can_switch_category_mode(self):
        profile = SupplierProfile.objects.create(user=self.user)
        response = self.client.post(
            reverse("crud:settings"),
            {"form_type": "category_mode", "category_mode": "single"},
        )
        self.assertEqual(response.status_code, 302)
        profile.refresh_from_db()
        self.assertEqual(profile.category_mode, "single")

    def test_single_category_mode_limits_product_categories(self):
        clothes = Category.objects.create(name="Clothes")
        categories = [
            clothes,
            Category.objects.create(name="Men", parent=clothes),
            Category.objects.create(name="Women", parent=clothes),
            Category.objects.create(name="Kids", parent=clothes),
        ]
        profile = SupplierProfile.objects.create(user=self.user, category_mode="single")

        form = ProductForm(supplier=profile)

        self.assertCountEqual(
            form.fields["category"].queryset.values_list("name", flat=True),
            [category.name for category in categories],
        )

    def test_shop_category_page_includes_descendant_products(self):
        clothes = Category.objects.create(name="Clothes")
        men = Category.objects.create(name="Men", parent=clothes)
        supplier = SupplierProfile.objects.create(user=self.user, category_mode="multiple")
        Product.objects.create(
            name="Shirt", category=men, supplier=supplier, price="10.00", status="active"
        )
        self.client.logout()

        response = self.client.get(reverse("shop:category", args=[clothes.slug]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Shirt")

    def test_shop_home_includes_legacy_products_without_supplier(self):
        category = Category.objects.create(name="Electronics")
        Product.objects.create(
            name="Legacy Phone", category=category, price="10.00", status="active"
        )
        self.client.logout()

        response = self.client.get(reverse("shop:home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Legacy Phone")

    def test_shop_home_limits_legacy_products_in_single_category_mode(self):
        clothes = Category.objects.create(name="Clothes")
        Category.objects.create(name="Men", parent=clothes)
        electronics = Category.objects.create(name="Electronics")
        Product.objects.create(
            name="Legacy Shirt", category=clothes, price="10.00", status="active"
        )
        Product.objects.create(
            name="Legacy Phone", category=electronics, price="20.00", status="active"
        )
        shop_user = get_user_model().objects.create_user("shop_mode_user", password="pw")
        SupplierProfile.objects.create(user=shop_user, category_mode="single")
        self.client.force_login(shop_user)

        response = self.client.get(reverse("shop:home"))

        self.assertContains(response, "Legacy Shirt")
        self.assertNotContains(response, "Legacy Phone")

    def test_public_shop_uses_latest_supplier_category_mode(self):
        clothes = Category.objects.create(name="Clothes")
        electronics = Category.objects.create(name="Electronics")
        Product.objects.create(
            name="Public Shirt", category=clothes, price="10.00", status="active"
        )
        Product.objects.create(
            name="Public Phone", category=electronics, price="20.00", status="active"
        )
        SupplierProfile.objects.create(user=self.user, category_mode="single")
        self.client.logout()

        response = self.client.get(reverse("shop:home"))

        self.assertContains(response, "Public Shirt")
        self.assertNotContains(response, "Public Phone")


class SeedAndRelationsTests(TestCase):
    def test_seed_demo_populates_relations_idempotently(self):
        call_command("seed_demo", "--no-superuser", verbosity=0)
        self.assertEqual(Company.objects.count(), 6)
        self.assertEqual(Contact.objects.count(), 24)
        self.assertEqual(Tag.objects.count(), 6)
        self.assertEqual(Project.objects.count(), 10)
        self.assertEqual(Task.objects.count(), 40)

        project = Project.objects.first()
        self.assertIsNotNone(project.company)          # FK
        self.assertEqual(project.team.count(), 4)      # M2M (team)
        self.assertTrue(project.tags.exists())         # M2M (tags)
        self.assertTrue(project.tasks.exists())        # reverse FK (tasks)
        self.assertTrue(Contact.objects.filter(company__isnull=False).exists())  # Contact -> Company

        call_command("seed_demo", "--no-superuser", verbosity=0)  # idempotent
        self.assertEqual(Project.objects.count(), 10)


class ProjectViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user("pv", password="pw", is_staff=True)
        call_command("seed_demo", "--no-superuser", verbosity=0)

    def setUp(self):
        self.client.force_login(self.user)

    def test_project_list_requires_login(self):
        self.client.logout()
        self.assertEqual(self.client.get(reverse("crud:project_list")).status_code, 302)

    def test_project_list_renders_themed_table(self):
        html = self.client.get(reverse("crud:project_list")).content.decode()
        self.assertIn('class="card"', html)        # AdminLTE tables2 theme
        self.assertIn("members", html)             # team-count column
        self.assertIn("All companies", html)       # django-filter select

    def test_project_detail_shows_relations(self):
        project = Project.objects.first()
        html = self.client.get(reverse("crud:project_detail", args=[project.pk])).content.decode()
        self.assertIn(project.name, html)
        self.assertIn(project.company.name, html)  # FK rendered
        self.assertIn("Team", html)                # M2M team panel
        self.assertIn("Tasks", html)               # reverse-FK tasks
