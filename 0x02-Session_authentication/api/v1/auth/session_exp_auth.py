#!/usr/bin/env python
"""
   Session Auth
"""
import os
from flask import Flask, request, jsonify, abort
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime


SESSION_DURATION = int(os.getenv('SESSION_DURATION', 0))


class SessionExpAuth(SessionAuth):
    """
       Extends SessionAuth
    """
    def __init__(self):
        self.session_duration = (SESSION_DURATION)

    def create_session(self, user_id=None):
        """
            Create a session id by calling super()
            super() will call create_session()

            Retrun 
                
                None If super() cant create a Session Id
            otherwise

                use this Session Id as a key of a dict 
                user_id_by_session_id and assign a dict
                as a value with user_idand created_at as a keys.
        """
        # Call SessionAuth create_session method to create Session Id
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        user_dict = {'user_id': user_id,
                        'created_at': datetime.now()
                     }
        # Assign the user_dict under session id act as key
        self.user_id_by_session_id[session_id] = user_dict

        return session_id

    def user_id_for_session(self, session_id=None):
        """
           Return 
              
              None if session_id is None
              None if user_id_by_session_id doesnt have key session_id
              user_id if self.session_duration <= 0
              None if session doesnt have key created_at
              None if created_at + session_duration before datetime - timedelta

           otherwise
              
              return user_id
        """
        if session_id is None:
            return None
        if not self.user_id_by_session_id.get(session_id):
            return None
        session_dictionary = self.user_id_by_session_id.get(session_id)
        if self.session_duration <= 0:
            return session_dictionary.get('user_id')
        if not session_dictionary.get('created_at'):
            return None
        created_at = session_dictionary.get('created_at')
        expiration_time = created_at + timedelta(seconds=self.session_duration)

        if datetime.now() > expiration_time:
            return None
        return session_dictionary.get('user_id')


