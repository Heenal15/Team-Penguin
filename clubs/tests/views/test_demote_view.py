"""Tests of the demote view."""
from django.test import TestCase
from django.urls import reverse
from clubs.models import User

class DemoteViewTestCase(TestCase):
    """Tests of the demote view."""

    fixtures = ['clubs/tests/fixtures/other_users.json']

    def setUp(self):
        self.user = User.objects.get(email = 'emilydoe@example.org')
        self.target_user = User.objects.get(email='mikedoe@example.org')
        self.url = reverse('demote', kwargs={'user_id': self.target_user.id})

    def test_demote_url(self):
        self.assertEqual(self.url,f'/demote/{self.target_user.id}')

    def test_demote_officer_to_member(self):
        before_count =  User.objects.filter(user_type = 1).count()
        self.client.login(email=self.user.email, password='Password123')
        url = reverse('demote', kwargs={'user_id': self.target_user.id})
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.target_user.refresh_from_db()
        after_count = User.objects.filter(user_type = 1).count()
        self.assertEqual(after_count, before_count+1)
        self.assertEqual(self.target_user.user_type, 1)

    def test_get_demote(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_get_demote_redirects_when_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
