import email
from operator import contains
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self):
        # In test we use the client to make requests to the admin page
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@gmail.com", password="test123"
        )
        # In test used from force_login instead of login that faster
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email="test@gmail.com", password="test123", name="Test user full name"
        )

    def test_users_listed(self):
        """Test that users are listed on user page"""
        # use reverse to get the url of the user page
        url = reverse("admin:core_user_changelist")
        # /admin/core/user
        # use the client to make a request to the url
        res = self.client.get(url)
        assert self.user.name in str(res.content)
        assert self.user.email in str(res.content)
    
    def test_user_page_change(self):
        """Test that the user edit page works"""
        # user reverse to get the url of the user edit page
        url = reverse("admin:core_user_change", args=[self.user.id])
        # /admin/core/user/1
        res = self.client.get(url)
        assert res.status_code == 200

    def test_create_user_page(self):
        """Test that the create user page works."""
        url = reverse("admin:core_user_add")
        res = self.client.get(url)
        assert res.status_code == 200
