"""Tests of the promote view."""
from django.test import TestCase
from django.urls import reverse
from clubs.models import User

class PromoteViewTestCase(TestCase):
    """Tests of the promote view."""

    fixtures = ['clubs/tests/fixtures/other_users.json']

    def setUp(self):
        self.user = User.objects.get(email = 'emilydoe@example.org')
        self.target_user = User.objects.get(email='lilydoe@example.org')
        self.url = reverse('promote', kwargs={'user_id': self.target_user.id})

    def test_promote_url(self):
        self.assertEqual(self.url,f'/promote/{self.target_user.id}')

    def test_promote_member_to_officer(self):
        before_count =  User.objects.filter(user_type = 2).count()
        self.client.login(email=self.user.email, password='Password123')
        url = reverse('promote', kwargs={'user_id': self.target_user.id})
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.target_user.refresh_from_db()
        after_count = User.objects.filter(user_type = 2).count()
        self.assertEqual(after_count, before_count+1)
        self.assertEqual(self.target_user.user_type, 2)

    def test_get_promote(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_get_promote_redirects_when_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
