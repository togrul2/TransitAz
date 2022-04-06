from django.db.utils import IntegrityError
from django.test import TestCase
from user.models import User

# Create your tests here.


class UserModelTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='test_user', email='example@example.com')
        user.set_password('abcde12345')

    def test_not_verified_by_default(self):
        user = User.objects.create_user(username='test_user_2')
        user.set_password('test_password')
        self.assertFalse(user.is_verified)

    def test_create_user_with_existing_username(self):
        self.assertRaises(IntegrityError, User.objects.create_user, username='test_user', email='example@example.com')
