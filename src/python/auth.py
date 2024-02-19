import re
import sqlite3
import hashlib
import uuid

DATABASE_NAME = 'user_db.db'


class UserManager:
    def __init__(self, db_path="user_db.db"):
        self.conn = sqlite3.connect(db_path)

    def is_valid_email(self, email: str) -> bool:
        return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

    def is_valid_password(self, password: str) -> bool:
        return len(password) >= 8

    def hash_password(self, password: str) -> str:
        """Generates the hash hex string of the password."""
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, email: str, password: str) -> str:
        """Registers users and upon successfully registration returns user id else raise value error."""

        if not self.is_valid_email(email) or not self.is_valid_password(password):
            raise ValueError("Invalid email or password")

        cursor = self.conn.cursor()

        cursor.execute('SELECT * FROM users WHERE email=?', (email,))
        existing_user = cursor.fetchone()
        if existing_user:
            raise ValueError('Email already registered')

        hashed_password = self.hash_password(password)

        activation_token = str(uuid.uuid4())

        cursor.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, hashed_password))

        self.conn.commit()

        return activation_token

    def authenticate_user(self, email: str, password: str) -> bool:
        """Authenticates user by their email and password."""

        cursor = self.conn.cursor()

        cursor.execute('SELECT * FROM users WHERE email=?', (email,))
        user = cursor.fetchone()

        if user and self.hash_password(password) == user[2]:
            return True
        else:
            return False
