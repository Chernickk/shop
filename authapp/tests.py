from django.test import TestCase
from django.test.client import Client
from django.core.management import call_command
from authapp.models import ShopUser


class TestAuthappSmoke(TestCase):
    def setUp(self) -> None:
        call_command('loaddata', 'test_db.json')
        self.client = Client()

        self.superuser = ShopUser.objects.create_superuser(
            'django_su',
            'django_su@test.com',
            'password1',
        )
        self.user = ShopUser.objects.create_user(
            'django_u',
            'django_u@test.com',
            'password2',
        )
        self.user_with_first_name = ShopUser.objects.create_user(
            'django_name',
            'django_name@test.com',
            'password3',
            first_name='django',
        )

    def test_user_login(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('/mainapp/index.html')
        self.assertTrue(response.context['user'].is_anonymous)

        self.client.login(username='django_u', password='password2')

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('/mainapp/index.html')
        self.assertFalse(response.context['user'].is_anonymous)
        self.assertEqual(response.context['user'], self.user)

        self.client.logout()
        response = self.client.get('/')
        self.assertTrue(response.context['user'].is_anonymous)

    def test_manual_register_login_logout(self):
        response = self.client.get('/')
        self.assertTrue(response.context['user'].is_anonymous)

        # User registration
        response = self.client.post(
            '/auth/register/',
            data={
                'username': 'djangotest',
                'first_name': 'testuser',
                'password1': '1oloLOtest1',
                'password2': '1oloLOtest1',
                'email': 'django@test.com',
            }
        )

        self.assertRedirects(response, '/')

        # Check new user is created
        new_user = ShopUser.objects.get(username='djangotest')

        # Skip email activation
        new_user.is_active = True
        new_user.save()

        response = self.client.get('/')
        self.assertTrue(response.context['user'].is_anonymous)

        # New user login
        response = self.client.post(
            '/auth/login/',
            data={
                'username': 'djangotest',
                'password': '1oloLOtest1',
            }
        )

        self.assertRedirects(response, '/')

        # Check if new user login successful
        response = self.client.get('/')
        self.assertEqual(response.context['user'], new_user)

        # Check logout
        self.client.get('/auth/logout/')
        response = self.client.get('/')
        self.assertTrue(response.context['user'].is_anonymous)





