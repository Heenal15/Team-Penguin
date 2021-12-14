"""Tests of the unapprove view."""
from django.test import TestCase
from django.urls import reverse
from clubs.models import User

class UnapproveViewTestCase(TestCase):
    """Tests of the unapprove view."""

    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.user = User.objects.get(email = 'mikedoe@example.org')
        self.target_user = User.objects.get(email='johndoe@example.org')
        self.url = reverse('unapprove', kwargs={'user_id': self.target_user.id})

    def test_unapprove_url(self):
        self.assertEqual(self.url,f'/unapprove/{self.target_user.id}')

    def test_unapprove_applicant(self):
        before_count =  User.objects.filter(user_type = 0).count()
        self.client.login(email=self.user.email, password='Password123')
        url = reverse('unapprove', kwargs={'user_id': self.target_user.id})
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        after_count = User.objects.filter(user_type = 0).count()
        self.assertEqual(after_count, before_count-1)
        self.assertEqual(self.target_user.user_type, 0)

    def test_get_unapprove(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_get_unapprove_redirects_when_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
