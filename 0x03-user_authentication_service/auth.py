#!/usr/bin/env python3
""" Contains the authentication functionalites"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """ Encrypts the password  and adds salt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
