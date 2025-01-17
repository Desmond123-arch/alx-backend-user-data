#!/usr/bin/env python3
""" Contains the authentication functionalites"""
from db import DB
from user import User
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _hash_password(password: str) -> bytes:
    """ Encrypts the password  and adds salt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """ Returns a  uuid as a string"""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Register a user to the database"""
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists.")
        except NoResultFound:
            new_user = self._db.add_user(email, _hash_password(password))
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """ Validates the users login"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)

    def create_session(self, email: str) -> str:
        """ Returns the session id as a string"""
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            setattr(user, 'session_id', session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """ Gets the user through the session id or returns none"""
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: str) -> None:
        """ Destroys a session / logs out a user"""
        if user_id is None:
            return None
        try:
            user = self._db.find_user_by(id=user_id)
            setattr(user, 'session_id', None)
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """ Used to token to reset the password"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        new_uuid = _generate_uuid()
        setattr(user, 'reset_token', new_uuid)
        return new_uuid

    def update_password(self, reset_token: str, password: str) -> None:
        """ Updates the users password """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        setattr(user, 'hashed_password', _hash_password(password))
        setattr(user, 'reset_token', None)
        return None
