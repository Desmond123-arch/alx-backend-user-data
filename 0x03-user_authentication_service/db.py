#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from user import User
from user import Base


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ Returns a user object """
        user = User(email=email, hashed_password=hashed_password)
        session = self._session
        session.add(user)
        session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """ Returns the first row found in the users """
        try:
            session = self.__session
            result = session.query(User).filter_by(**kwargs).one()
            return result
        except NoResultFound:
            raise NoResultFound
        except KeyError:
            raise InvalidRequestError

    def update_user(self, user_id, **kwargs):
        """ Updates the user with the various kwargs values"""
        try:
            session = self.__session
            session.query(User).filter_by(id=user_id).update({**kwargs})
            session.commit()
            return None
        except KeyError:
            session.rollback()
            raise ValueError
