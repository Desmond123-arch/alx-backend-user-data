#!/usr/bin/env python3
""" Basic auth class """
from typing import TypeVar
from api.v1.auth.auth import Auth
import base64
import binascii
from api.v1.views.users import User
from api.v1.auth.auth import Auth

class BasicAuth(Auth):
    """ The basic authentication class """

    def extract_base64_authorization_header(self, authorization_header: str)\
            -> str:
        """ Extracts the base 64 string """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split('Basic ', 1)[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """Decodes the authorization header"""
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except binascii.Error:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """ Extracts the user credientials by decoding """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(
                decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        return tuple(
            decoded_base64_authorization_header.split(':'))

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """ Returns the User instance based on his email and password"""
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        if len(User.all()) == 0 or\
                len(User.search({"email": user_email})) == 0:
            return None
        user = User.search({"email": user_email})[0]
        if not user.is_valid_password(pwd=user_pwd):
            return None
        return user
    
    def current_user(self, request=None) -> TypeVar('User'):
        """ Retireve the current user instance for a request """
        if request is None:
            return None
        auth = Auth()
        header = auth.authorization_header(request)
        val = self.extract_base64_authorization_header(header)
        decoded = self.decode_base64_authorization_header(val)
        user, pwd = self.extract_user_credentials(decoded)
        return self.user_object_from_credentials(user, pwd)