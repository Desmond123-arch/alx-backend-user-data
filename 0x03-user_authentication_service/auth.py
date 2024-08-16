#!/usr/bin/env python3
""" Contains the authentication functionalites"""
from db import DB
from user import User
import bcrypt
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """ Encrypts the password  and adds salt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Register a user to the database"""
        session = self._db._session
        try:
            user = session.query(User).filter_by(email=email).one()
        except NoResultFound:
            raise ValueError(f"User {email} already exists.")
        new_user = User(email=email, hashed_password=_hash_password(password))
        session.commit()
        return new_user
