#!/usr/bin/env python3
"""" Contains the user class """
from base import Base
from sqlalchemy import Column, Integer, String


class User(Base):
    """ Users class for the database """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=False)
    reset_token = Column(String(250), nullable=False)
