#!/usr/bin/env python3
"""Hash Function"""
import bcrypt
from db import DB
from user import User


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a user with email and password"""
        search_query = {'email': email}

        try:
            user_found = self._db.find_user_by(**search_query)
        except Exception:
            # Hash the user password and add to the database
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user

        raise ValueError('User {} already exists.'.format(email))


def _hash_password(password: str) -> bytes:
    """takes in a password string arguments and returns bytes."""
    # Convert password to bytes
    pwd_in_byte = password.encode('utf-8')
    # Generate a salt
    pwd_salt = bcrypt.gensalt()
    # Hash the password
    hashed_password = bcrypt.hashpw(pwd_in_byte, pwd_salt)
    return hashed_password
