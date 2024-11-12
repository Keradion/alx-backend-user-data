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
    def  extract_base64_authorization_header(self, authorization_header: str) -> str:
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

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
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

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        """Extract username and password from Base64 decoded value"""
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if not ':' in decoded_base64_authorization_header:
            return (None, None)
        # Extract user email and password 
        useremail_passwd = tuple(decoded_base64_authorization_header.split(':'))
        return useremail_passwd




    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
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

        return user[0]
