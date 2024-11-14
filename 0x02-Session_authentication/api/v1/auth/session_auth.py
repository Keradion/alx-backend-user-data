#!/usr/bin/env python3
"""SessionAuth class"""
import uuid
import os
from flask import request
from api.v1.auth.auth import Auth

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

    def session_cookie(self, request=None) -> str:
        """
           Return 
               
               None If request is None

           otherwise

              Return the value of _my_session_id cookie from request
              SESSION_NAME env variable holds the cookie
        """
        if request is None:
            return 
        
        # Read the cookie name from the env variable
        cookie_name = getenv('SESSION_NAME')

        # Acess the the value of cookie_name from the cookie
        cookie_value = request.cookie.get(cookie_name)
        
        return cookie_value
