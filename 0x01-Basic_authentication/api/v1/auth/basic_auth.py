#!/usr/bin/env python3
""" Basic auth class """
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """ The basic authentication class """

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """ Extracts the base 64 string """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split('Basic', 1)[1]
