from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import CustomerProfile

# Create your tests here.


class ShopLogoutTests(TestCase):
	def test_shop_logout_works_from_an_existing_page(self):
		user = get_user_model().objects.create_user("customer", password="pw-12345!")
		CustomerProfile.objects.create(user=user)
		self.client.force_login(user)

		response = self.client.get(reverse("shop:logout"))

		self.assertRedirects(response, reverse("shop:home"))
		self.assertNotIn("_auth_user_id", self.client.session)
