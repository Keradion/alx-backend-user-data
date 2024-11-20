#!/usr/bin/env python3
"""Hash Function"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """takes in a password string arguments and returns bytes."""
    # Convert password to bytes
    pwd_in_byte = password.encode('utf-8')

    # Generate a salt
    pwd_salt = bcrypt.gensalt()

    # Hash the password
    hashed_password = bcrypt.hashpw(pwd_in_byte, pwd_salt)

    return hashed_password
