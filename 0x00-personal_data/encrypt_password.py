#!/usr/bin/env python3
"""Password hashing"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Returns salted hashed_password """
    # Convert password to bytes
    byte = password.encode('utf-8')

    # generat salt
    salt = bcrypt.gensalt()

    # Hash the password
    hashed_password = bcrypt.hashpw(byte, salt)

    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """validate the hashed_password with the orginal password provided"""
    # Encode password to utf-8 before check
    password = password.encode('utf-8')

    # Check if the hashed_password is valid
    if bcrypt.checkpw(password, hashed_password):
        return True
    return False
