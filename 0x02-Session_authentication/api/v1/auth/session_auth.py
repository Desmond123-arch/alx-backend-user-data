#!/usr/bin/env python3
""" Contains the session authentication class """
from api.v1.auth.auth import Auth
from api.v1.views.users import User
from typing import TypeVar
from uuid import uuid4
import os


class SessionAuth(Auth):
    """Contains the session auth class"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Creates the user session object"""
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        session_id = str(uuid4())
        SessionAuth.\
            user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self,
                               session_id: str = None) -> str:
        """ Retireves the user id through the session id"""
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None
        return SessionAuth.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> TypeVar('User'):
        """ Returns the current user through the session id"""
        cookie = self.session_cookie(request)
        user_id = self.user_id_by_session_id.get(cookie)
        return User.get(user_id)

    def destroy_session(self, request=None):
        """ Deletes the user session/ logout"""
        if request is None:
            return False
        if not self.session_cookie(request):
            return False
        key = self.user_id_for_session_id(self.session_cookie(request))
        if not key:
            return False
        self.user_id_by_session_id.pop(key)
        return True
