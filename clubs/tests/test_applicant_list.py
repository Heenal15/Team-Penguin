from django.test import TestCase, RequestFactory
from django.urls import reverse
from clubs.models import User
from django.contrib.auth.models import AnonymousUser

class ApplicantListTest(TestCase):
    def setUp(self):
        self.url = reverse('applicant_list')
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            first_name = 'John',
            last_name = 'Doe',
            email = 'johndoe@example.org',
            bio = 'Hello, I am John Doe',
            password = 'Password123',
            is_active = True,
            user_type = 2
        )

    def test_applicant_list_url(self):
        self.assertEqual(self.url,'/applicants/')

    def test_get_applicant_list_as_anonymous_user(self):
        request = self.factory.get('/')
        request.user = AnonymousUser()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_get_applicant_list_as_authorised_user(self):
        request = self.factory.get('/')
        request.user = self.user
        self._create_test_applicants(5)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'applicant_list.html')
        self.assertEqual(len(response.context['applicants']), 5)
        for user_id in range(5):
            self.assertContains(response, f'Email{user_id}')
            self.assertContains(response, f'First{user_id}')
            self.assertContains(response, f'Last{user_id}')
            user = User.objects.get(email=f'Email{user_id}')
            user_url = reverse('show_user', kwargs={'user_id': user.id})
            self.assertContains(response, user_url)

    def _create_test_applicants(self, user_count=5):
        for user_id in range(user_count):
            User.objects.create_user(f'Email{user_id}@test.org',
                password='Password123',
                first_name=f'First{user_id}',
                last_name=f'Last{user_id}',
                bio=f'Bio {user_id}',
                experience=f'Experience {user_id}',
                statement=f'Statement {user_id}',
            )