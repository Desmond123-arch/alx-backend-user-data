#!/usr/bin/env python3
""" Contains the session authentication class """
from api.v1.auth.auth import Auth
from uuid import uuid4


class SessionAuth(Auth):
    """Contains the session auth class"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Creates the user session object"""
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        session_id = uuid4()
        SessionAuth.\
            user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self,
                               session_id: str = None) -> str:
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None
        return SessionAuth.\
            user_id_by_session_id.get(session_id)
