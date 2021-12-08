from django.test import TestCase, Client
from django.urls import reverse
from clubs.models import User

class MemberListTest(TestCase):
    def setUp(self):
        self.url = reverse('member_list')
        self.user = User.objects.create_user(
            first_name = 'John',
            last_name = 'Doe',
            email = 'johndoe@example.org',
            password = 'Password123',
            bio = 'Hello, I am John Doe',
            is_active = True,
            user_type = 1
        )
        self.client = Client()

    def test_member_list_url(self):
        self.assertEqual(self.url,'/members/')

    def test_get_member_list_as_anonymous_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_get_member_list_as_authorised_user(self):
        self.client.login(email='johndoe@example.org', password='Password123')
        self._create_test_members(5-1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'member_list.html')
        self.assertEqual(len(response.context['users']), 5)
        for user_id in range(5-1):
            self.assertContains(response, f'Email{user_id}')
            self.assertContains(response, f'First{user_id}')
            self.assertContains(response, f'Last{user_id}')
            user = User.objects.get(username=f'Email{user_id}')
            user_url = reverse('show_user', kwargs={'user_id': user.id})
            self.assertContains(response, user_url)

    def _create_test_members(self, user_count=5):
        for user_id in range(user_count):
            User.objects.create_user(f'Email{user_id}',
                password='Password123',
                first_name=f'First{user_id}',
                last_name=f'Last{user_id}',
                bio=f'Bio {user_id}',
                experience=f'Experience {user_id}',
                statement=f'Statement {user_id}',
            )
