#!/usr/bin/env python3
"""SessionAuth class"""
import uuid
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
