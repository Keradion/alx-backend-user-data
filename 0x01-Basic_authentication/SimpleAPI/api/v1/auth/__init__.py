#!/usr/bin/python3
""" Class to manage the API authentication """
from flask import request
from typing import List, TypeVar

class Auth:
    """Template for all authentication system"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Returns true if path is in exluded_paths otherwise false"""
        return False
    

    def authorization_header(self, request=None) -> str:
        """"""
        return None


    def current_user(self, request=None) -> TypeVar('User'):
        """"""
        return None
