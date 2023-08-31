from django.contrib.auth import get_user
from django.test import TestCase
from django.urls import reverse
from .models import User


class RegistrationTestCase(TestCase):
    def test_user_account_is_created(self):
        self.client.post(
            reverse('users:register'),
            # '/users/register/', # url_name
            data={
                'username': "farhodjon",
                'email': 'farhodjonhikmatullayev@gmail.com',
                'password': "Pass@123",
            }
        )
        user = User.objects.get(username='farhodjon')

        self.assertEqual(user.email, 'farhodjonhikmatullayev@gmail.com')
        self.assertNotEqual(user.password, 'Pass@123')
        self.assertTrue(user.check_password("Pass@123"))

    def test_required_fields(self):
        response = self.client.post(
            reverse('users:register'),
            data={
                'email': 'farhodjonhikmatullayev@gmail.com'
            }
        )
        users_count = User.objects.count()
        self.assertEqual(users_count, 0)
        self.assertFormError(response, 'form', 'username', 'This field is required.')
        self.assertFormError(response, 'form', 'password', 'This field is required.')

    def test_invalid_email(self):
        response = self.client.post(
            reverse('users:register'),
            data={
                'username': "farhodjon",
                'email': 'farhodjonhikmatulla',
                'password': "Pass@123",
            }
        )

        users_count = User.objects.count()
        self.assertEqual(users_count, 0)
        self.assertFormError(response, 'form', 'email', 'Enter a valid email address.')

    def test_unique_username(self):
        self.client.post(
            reverse('users:register'),
            data={
                'username': "farhodjon",
                'email': 'farhodjonhikmatullayev@gmil.com',
                'password': "Pass@123",
            }
        )
        users_count = User.objects.count()
        self.assertEqual(users_count, 1)

        response = self.client.post(
            reverse('users:register'),
            data={
                'username': "farhodjon",
                'email': 'farhodjonhikmatullayev@gmil.com',
                'password': "Pass@123",
            }
        )
        users_count2 = User.objects.count()
        self.assertEqual(users_count2, 1)
        self.assertFormError(response, 'form', 'username', 'A user with that username already exists.')


class LoginTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username="farhodjon", email="aaa@gmail.com")
        user.set_password('Pass@123')
        user.save()

    def test_success_login(self):
        self.client.post(
            reverse('users:login'),
            data={
                'username': 'farhodjon',
                'password': 'Pass@123'
            }
        )

        user = get_user(self.client)

        self.assertTrue(user.is_authenticated)

    def test_wrong_fields(self):
        self.client.post(
            reverse('users:login'),
            data={
                'username': 'farhodjo',
                'password': 'Pass@123'
            }
        )
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

        self.client.post(
            reverse('users:login'),
            data={
                'username': 'farhodjon',
                'password': 'Pass@12'
            }
        )
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

    def test_logout(self):
        self.client.login(username='farhodjon', password='Pass@123')
        response = self.client.get(reverse('users:logout'))
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)


class ProfileTestCase(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.url, reverse('users:login') + '?next=/users/profile/')
        self.assertEqual(response.status_code, 302)

    def test_profile(self):
        user = User.objects.create(username='farhodjon', email='farhodjonhikmatullayev@gmail.com')
        user.set_password('Pass@123')
        user.save()
        self.client.login(username='farhodjon', password='Pass@123')

        response = self.client.get(reverse('users:profile'))
        self.assertContains(response, user.username)
        self.assertContains(response, user.email)
        self.assertEqual(response.status_code, 200)

    def test_edit_profile(self):
        user = User.objects.create(username='farhodjon', email='farhodjonhikmatullayev@gmail.com')
        user.set_password('Pass@123')
        user.save()
        self.client.login(username='farhodjon', password='Pass@123')
        response = self.client.post(
            reverse('users:profile_edit'),
            data={
                'username': 'farhod',
                'first_name': 'Farhodjon',
                'last_name': 'Hikmatullayev',
                'email': 'farhod@gmail.com',
            }
        )
        user.refresh_from_db()  # yangilangan user objectini olib beradi
        # user = User.objects.get(id=user.id)
        self.assertEqual(user.email, 'farhod@gmail.com')
        self.assertEqual(user.username, 'farhod')
        self.assertEqual(user.first_name, 'Farhodjon')
        self.assertEqual(user.last_name, 'Hikmatullayev')
        self.assertEqual(response.url, reverse('users:profile'))
