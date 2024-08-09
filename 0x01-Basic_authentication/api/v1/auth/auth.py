#!/usr/bin/env python3
""" Contains the api authentication class"""

from typing import TypeVar, List
from flask import request


class Auth:
    """ Authentication class """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """  Returns false-path for now"""
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path in excluded_paths or (path + '/') in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """ Return now, request will be a flask object"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Current user object"""
        return None
