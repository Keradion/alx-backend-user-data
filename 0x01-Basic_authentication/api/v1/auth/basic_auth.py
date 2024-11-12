#!/usr/bin/env python3
"""
BasicAuth Class 
"""
from api.v1.auth.auth import Auth


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


