#!/usr/bin/env python3
"""
BasicAuth Class
"""
import base64
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """Inherits Auth"""
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
           Returns Base64 part of the Authorization header for
           Basic Authentication.
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None

        # check if authorization_header starts with 'Basic'
        starts_with_basic = authorization_header.startswith('Basic ', 0, )

        if not starts_with_basic:
            return None

        # slice and return the remaining string sub part after 'Basic'
        return authorization_header[6::]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """
           Retruns the decoded value of a Base64 string
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            # Convert Base64 string to bytes
            base64_bytes = base64.b64decode((base64_authorization_header))
            # Convert the byte and return string
            return base64_bytes.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> (str, str):
        """Extract username and password from Base64 decoded value"""
        user_email = ''
        user_pwd = ''
        counter = 0

        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        for char in decoded_base64_authorization_header:
            if char != ':':
                user_email = user_email + char
                counter += 1
            # user_email extraction done
            if char == ':':
                break

        user_pwd = decoded_base64_authorization_header[len(user_email) + 1::]
        return (user_email, user_pwd)

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """Returns the User instance based on his email and password"""
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        # Check If the database consist user with user_email
        user_email = {'email': user_email}
        user = User.search(user_email)
        if not user:
            return None

        # check if the user_pwd is valid and associated with user
        # since search returns a list
        for each_user in user:
            is_valid_pwd = each_user.is_valid_password(user_pwd)
            if not is_valid_pwd:
                return None

        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """overloads Auth and retrieves the User instance for a request"""
        auth_header = self.authorization_header(request)

        if auth_header is not None:
            auth_base64 = self.extract_base64_authorization_header(
                    auth_header)
            if auth_base64 is not None:
                base64_decoded = self.decode_base64_authorization_header(
                        auth_base64)
                if base64_decoded is not None:
                    user_email, user_pwd = self.extract_user_credentials(
                            base64_decoded)
                    if user_email is not None:
                        user = self.user_object_from_credentials(
                                user_email, user_pwd)
                    if user is not None:
                        return user
        return
