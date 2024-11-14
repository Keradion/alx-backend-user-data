#!/usr/bin/env python3
""" Class to manage the API authentication """
from flask import request
from typing import List, TypeVar


class Auth:
    """Template for all authentication system"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
           Returns true if path is in excluded_paths otherwise false
           The method is slash tolerant meaning path=/api/v1/status and
           path=/api/v1/status/ must be treated as same.
        """
        if path is None or (excluded_paths is None or excluded_paths == []):
            return True

        if not path.endswith('/'):
            path = path + '/'

        for each in excluded_paths:
            if each[len(each) - 1] == '*':
                index = each.index('*')
                main_path = each[0:index]
                if main_path in path:
                    return False
            if not each.endswith('/'):
                each = each + '/'
            if path == each:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
           Returns None if request does not contain Authorization
           and return the value of the header request Authorization
        """
        if request is None:
            return None

        # Fetch the value under Authorization header key
        authorization = request.headers.get('Authorization')
        if authorization is None:
            return None
        return authorization

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns none and used to"""
        return None
