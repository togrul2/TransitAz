from django.db.utils import IntegrityError
from django.test import TestCase
from user.models import User


class TestUserModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', email='example@example.com')
        self.user.set_password('abcde12345')

    def test_not_verified_by_default(self):
        self.assertFalse(self.user.is_verified)

    def test_create_user_with_existing_username(self):
        self.assertRaises(IntegrityError, User.objects.create_user, username='test_user', email='example@example.com')
