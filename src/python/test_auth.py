import unittest
import os

from auth import UserManager
from db import create_table


class TestUserManager(unittest.TestCase):

    def setUp(self):
        self.db_path = 'test_user_db.db'
        create_table(self.db_path)
        self.user_manager = UserManager(self.db_path)

    def tearDown(self):
        self.user_manager.conn.close()
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_is_valid_email_valid(self):
        self.assertTrue(self.user_manager.is_valid_email("user@example.com"))

    def test_is_valid_email_invalid(self):
        self.assertFalse(self.user_manager.is_valid_email("invalidemail"))

    def test_is_valid_password_valid(self):
        self.assertTrue(self.user_manager.is_valid_password("password123"))

    def test_is_valid_password_invalid(self):
        self.assertFalse(self.user_manager.is_valid_password("pass"))

    def test_hash_password(self):
        hashed_password = self.user_manager.hash_password("password123")
        self.assertIsNotNone(hashed_password)
        self.assertNotEqual(hashed_password, "password123")

    def test_register_user_valid(self):
        activation_token = self.user_manager.register_user("user@example.com", "password123")
        self.assertIsNotNone(activation_token)

    def test_register_user_invalid_email(self):
        with self.assertRaises(ValueError):
            self.user_manager.register_user("invalidemail", "password123")

    def test_register_user_invalid_password(self):
        with self.assertRaises(ValueError):
            self.user_manager.register_user("user@example.com", "pass")

    def test_register_user_existing_email(self):
        self.user_manager.register_user("user@example.com", "password123")
        with self.assertRaises(ValueError):
            self.user_manager.register_user("user@example.com", "anotherpassword")

    def test_authenticate_user_valid_credentials(self):
        self.user_manager.register_user("user@example.com", "password123")
        authenticated = self.user_manager.authenticate_user("user@example.com", "password123")
        self.assertTrue(authenticated)

    def test_authenticate_user_invalid_password(self):
        self.user_manager.register_user("user@example.com", "password123")
        authenticated = self.user_manager.authenticate_user("user@example.com", "wrongpassword")
        self.assertFalse(authenticated)


if __name__ == '__main__':
    unittest.main()
