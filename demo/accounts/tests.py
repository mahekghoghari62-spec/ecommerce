from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from crud.models import PanelUser
from shop.models import CustomerProfile


class AllauthThemeTests(TestCase):
    """The package's AdminLTE-themed allauth layouts/elements render + work."""

    def test_login_page_uses_adminlte_theme(self):
        resp = self.client.get(reverse("account_login"))
        self.assertEqual(resp.status_code, 200)
        html = resp.content.decode()
        self.assertIn("login-box", html)                                # AdminLTE auth card
        self.assertIn("adminlte/dist/css/adminlte.min.css", html)       # self-hosted bundle
        self.assertIn("form-control", html)                             # BS5 fields (themed elements)
        self.assertIn("btn btn-primary", html)                          # themed submit button
        self.assertNotIn("<p><label", html)                            # not allauth's default as_p

    def test_signup_page_themed(self):
        html = self.client.get(reverse("account_signup")).content.decode()
        self.assertIn("login-box", html)
        self.assertIn("form-control", html)

    def test_themed_login_actually_authenticates(self):
        get_user_model().objects.create_user("alice", password="pw-12345")
        resp = self.client.post(reverse("account_login"), {"login": "alice", "password": "pw-12345"})
        self.assertEqual(resp.status_code, 302)                         # logged in -> redirect
        self.assertIn("_auth_user_id", self.client.session)


class DemoLoginPageTests(TestCase):
    """The demo's own /login/ page pre-fills the seeded credentials and explains
    the layout, and bounces already-authenticated visitors to the dashboard."""

    def test_login_page_prefills_demo_credentials(self):
        resp = self.client.get(reverse("login"))
        self.assertEqual(resp.status_code, 200)
        html = resp.content.decode()
        self.assertIn('value="admin"', html)          # username pre-filled
        self.assertIn('value="adminpass"', html)       # password pre-filled
        self.assertIn("Demo account", html)            # credentials callout
        self.assertIn("Django admin", html)            # structure tour

    def test_authenticated_user_can_switch_to_admin_login(self):
        get_user_model().objects.create_user("tester", password="pw-12345!")
        self.client.login(username="tester", password="pw-12345!")
        resp = self.client.get(reverse("login"))
        self.assertEqual(resp.status_code, 200)

    def test_customer_cannot_login_to_admin_panel(self):
        customer = get_user_model().objects.create_user("customer", password="pw-12345!")
        CustomerProfile.objects.create(user=customer)

        response = self.client.post(
            reverse("login"),
            {"username": "customer", "password": "pw-12345!"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_panel_user_cannot_login_to_shop(self):
        panel_user = get_user_model().objects.create_user(
            "panel", password="pw-12345!", is_staff=True
        )
        PanelUser.objects.create(user=panel_user, full_name="Panel User")

        response = self.client.post(
            reverse("shop:login"),
            {"username": "panel", "password": "pw-12345!"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_non_staff_account_can_login_to_shop(self):
        get_user_model().objects.create_user("shopuser", password="pw-12345!")

        response = self.client.post(
            reverse("shop:login"),
            {"username": "shopuser", "password": "pw-12345!"},
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("shop:home"))

    def test_panel_user_can_login_to_admin_panel(self):
        panel_user = get_user_model().objects.create_user(
            "panel", password="pw-12345!", is_staff=True
        )
        PanelUser.objects.create(user=panel_user, full_name="Panel User")

        response = self.client.post(
            reverse("login"),
            {"username": "panel", "password": "pw-12345!"},
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse(settings.LOGIN_REDIRECT_URL))

    def test_staff_session_is_removed_when_opening_shop(self):
        panel_user = get_user_model().objects.create_user(
            "panel", password="pw-12345!", is_staff=True
        )
        PanelUser.objects.create(user=panel_user, full_name="Panel User")
        self.client.force_login(panel_user)

        response = self.client.get(reverse("shop:home"))

        self.assertEqual(response.status_code, 200)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_legacy_logout_post_works_with_stale_page(self):
        user = get_user_model().objects.create_user("legacy", password="pw-12345!")
        self.client.force_login(user)
        csrf_client = self.client.__class__(enforce_csrf_checks=True)
        csrf_client.cookies = self.client.cookies

        response = csrf_client.post(reverse("logout"))

        self.assertRedirects(response, reverse("login"))
        self.assertNotIn("_auth_user_id", csrf_client.session)
