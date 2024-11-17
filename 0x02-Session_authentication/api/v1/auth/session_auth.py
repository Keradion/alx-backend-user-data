#!/usr/bin/env python3
"""SessionAuth class"""
import uuid
import os
from flask import request
from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """Inhertis From Auth, session based authorization"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Return:
                None If user_id is None
                None If user_id is not a string
        otherwise
                Generate a Session Id using uuid4()
                use this session id as a key to store
                user_id inside dict user_id_by_session.

           Return: Session Id generated
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        # Generate a Session Id
        session_id = str(uuid.uuid4())

        # Store user_id in user_id_by_session using session_id as key
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
           Retrun

           None If session_id is None
           None If session_id is not a string
           otherwise

           Retrun the value of user_id for key session_id
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        # Retrieve a user_id associated with session_id key
        user_id = self.user_id_by_session_id.get(session_id)

        return user_id

    def current_user(self, request=None) -> 'User':
        """
           Returns a User Instance associate with session_id
           based on a cookie value
        """
        # Get the session_id from cookies
        session_id = self.session_cookie(request)

        if session_id:
            # Get user_id from session_id
            user_id = self.user_id_for_session_id(session_id)
            if user_id:
                user = User.get(user_id)
                if user:
                    return user
        return

    def destroy_session(self, request=None) -> '{}':
        """
        Retrun

        None If request is None
        False If request does not contain Session Id cookie
        False If session Id does not linked with any user id
        otherwise
              delete a user session id from user_id_by_session_id
              and return True.

        """
        if request is None:
            return None

        # check if request contain session_id cookie
        cookie_name = os.getenv('SESSION_NAME')
        session_id = request.cookies.get(cookie_name)

        if session_id is None:
            return False

        # check if the session_id linked with any user
        user_id = self.user_id_for_session_id(session_id)

        if user_id is None:
            return False

        del self.user_id_by_session_id[session_id]
        return True
