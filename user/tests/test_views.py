from django.test import TestCase
from django.test import Client
from django.urls import reverse
from user.models import User


class TestRegister(TestCase):
    def setUp(self):
        self.client = Client()

    def test_register_with_different_passwords(self):
        response = self.client.post(reverse('register'), {
            'first_name': 'john',
            'last_name': 'doe',
            'email': 'johndoe@example.com',
            'username': 'johndoe',
            'password1': 'abcde123',
            'password2': 'abcde124',
            'accepted': 'on'
        })
        self.assertEquals(response.status_code, 400)

    def test_with_invalid_emails(self):
        emails = (
            'example',
            '@gmail.com',
            'example@.com',
            'example@com',
            'example@com.'
        )
        for email in emails:
            with self.subTest(email=email):
                response = self.client.post(reverse('register'), {
                    'first_name': 'john',
                    'last_name': 'doe',
                    'email': email,
                    'username': 'johndoe',
                    'password1': 'abcde123',
                    'password2': 'abcde123',
                    'accepted': 'on'
                })
                self.assertEquals(response.status_code, 400)

    def test_with_invalid_passwords(self):
        passwords = ('11313131', 'test', 'johndoe')
        for password in passwords:
            with self.subTest(password=password):
                response = self.client.post(reverse('register'), {
                    'first_name': 'john',
                    'last_name': 'doe',
                    'email': 'johndoe@example.com',
                    'username': 'johndoe',
                    'password1': password,
                    'password2': password,
                    'accepted': 'on'
                })
                self.assertEquals(response.status_code, 400)

    def test_with_existing_username(self):
        usernames = ('johndoe', 'Johndoe', 'JOHNDOE')
        User.objects.create_user(username='johndoe')
        for username in usernames:
            with self.subTest(username=username):
                response = self.client.post(reverse('register'), {
                    'first_name': 'john',
                    'last_name': 'doe',
                    'email': 'johndoe@example.com',
                    'username': username,
                    'password1': 'password',
                    'password2': 'password',
                    'accepted': 'on'
                })
                self.assertEquals(response.status_code, 400)

    def test_with_existing_email(self):
        User.objects.create_user(username='johndoe', email='johndoe@example.com')
        response = self.client.post(reverse('register'), {
            'first_name': 'john',
            'last_name': 'doe',
            'email': 'johndoe@example.com',
            'username': 'johndoe',
            'password1': 'password',
            'password2': 'password',
            'accepted': 'on'
        })
        self.assertEquals(response.status_code, 400)

    def test_with_missing_accept(self):
        response = self.client.post(reverse('register'), {
            'first_name': 'john',
            'last_name': 'doe',
            'email': 'johndoe@example.com',
            'username': 'username',
            'password1': 'password',
            'password2': 'password'
        })
        self.assertEquals(response.status_code, 400)


class TestLogin(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='johndoe')
        self.user.set_password('Password123')

    def test_with_invalid_credentials(self):
        response = self.client.post(reverse('login'), {
            'username': 'johndoe',
            'password': 'password134'
        })
        self.assertEquals(response.status_code, 400)

    def test_with_unverified(self):
        response = self.client.post(reverse('login'), {
            'username': 'johndoe',
            'password': 'Password123'
        })
        self.assertEquals(response.status_code, 400)

    def test_success(self):
        self.user.is_verified = True
        self.user.save()
        response = self.client.post(reverse('login'), {
            'username': 'johndoe',
            'password': 'Password123'
        })
        self.assertEquals(response.status_code, 302)
        