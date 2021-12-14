"""Tests of the officer list view."""
from django.test import TestCase, Client
from django.urls import reverse
from clubs.models import User

class OfficerListTest(TestCase):
    """Tests of the officer list view."""

    fixtures = ['clubs/tests/fixtures/other_users.json']

    def setUp(self):
        self.url = reverse('officers')

        self.user = User.objects.get(email='emilydoe@example.org')
        self.client = Client()

    def test_officer_list_url(self):
        self.assertEqual(self.url,'/officers/')

    def deny_access_officer_list_to_anonymous_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_get_officer_list_as_authorised_user(self):
        self.client.login(email=self.user.email, password='Password123')
        self._create_test_officers(15-1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'officers.html')
        self.assertEqual(len(response.context['officers']), 15)
        for user_id in range(15-1):
            self.assertContains(response, f'Email{user_id}@test.org')
            self.assertContains(response, f'First{user_id}')
            self.assertContains(response, f'Last{user_id}')
            user = User.objects.get(email=f'Email{user_id}@test.org')
            user_url = reverse('show_user', kwargs={'user_id': user.id})
            self.assertContains(response, user_url)

    def _create_test_officers(self, user_count=4):
        for user_id in range(user_count):
            User.objects.create_user(f'Email{user_id}@test.org',
                password='Password123',
                first_name=f'First{user_id}',
                last_name=f'Last{user_id}',
                bio=f'Bio {user_id}',
                experience=f'Experience {user_id}',
                statement=f'Statement {user_id}',
                user_type = 2
            )
