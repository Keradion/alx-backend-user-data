#!/usr/bin/env python3
"""
BasicAuth Class 
"""
import base64
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



