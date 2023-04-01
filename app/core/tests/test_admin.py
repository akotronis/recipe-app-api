"""
Tests for the Django Admin modifications
"""
from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

class AdminSiteTests(TestCase):
    """Tests for Django Admin"""

    # Needs to be camelCase or it will break
    def setUp(self):
        """Create user and client"""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='testpass123',
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            password='testpass123',
            name='Test User',
        )

    def test_users_list(self):
        """Test Users are listed on page"""
        # Check Reversing Django Admin URLs
        url = reverse('admin:core_user_changelist')
        # We have logged in as admin in setUp
        res = self.client.get(url)
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)