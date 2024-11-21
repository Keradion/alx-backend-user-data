#!/usr/bin/env python3
"""Hash Function"""
import bcrypt
import uuid
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from typing import Union


def _generate_uuid() -> str:
    """ Generate and return UUID in string format."""
    return str(uuid.uuid4())


def _hash_password(password: str) -> bytes:
    """takes in a password string arguments and returns bytes."""
    # Convert password to bytes
    pwd_in_byte = password.encode('utf-8')
    # Generate a salt
    pwd_salt = bcrypt.gensalt()
    # Hash the password
    hashed_password = bcrypt.hashpw(pwd_in_byte, pwd_salt)
    return hashed_password


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

    def valid_login(self, email: str, password: str) -> bool:
        """ check password validity """
        search_query = {'email': email}
        try:
            user_found = self._db.find_user_by(**search_query)
            hashed_password = user_found.hashed_password
            check_pwd = bcrypt.checkpw(password=password.encode(),
                                       hashed_password=hashed_password
                                       )
            if check_pwd:
                return True
            else:
                return False
        except Exception:
            return False

    def create_session(self, email: str) -> str:
        """
           Create a session id and store it in the db
           as the user's session_id.
        """
        search_query = {'email': email}
        try:
            user = self._db.find_user_by(**search_query)
            session_id = _generate_uuid()
            setattr(user, 'session_id', session_id)
            return session_id
        except Exception:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """ Get a user associated with a session_id"""
        if session_id is None:
            return None

        search_query = {'session_id': session_id}
        try:
            user = self._db.find_user_by(**search_query)
            if user:
                return user
        except Exception:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Updates the corresponding user's session_id to None"""
        search_query = {'id': user_id}
        try:
            user = self._db.find_user_by(**search_query)
            self._db.update_user(user.id, session_id=None)
        except NoResultFound:
            return None
        return None

    def get_reset_password_token(self, email: str) -> str:
        """generate a reset token for a user associated with email."""
        search_query = {'email': email}
        try:
            user = self._db.find_user_by(**search_query)
        except NoResultFound:
            raise ValueError
        reset_token = _generate_uuid()
        update_query = {'reset_token': reset_token}
        self._db.update_user(user.id, **update_query)
        return reset_token
