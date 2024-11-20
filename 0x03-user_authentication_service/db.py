#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User


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
        """Add a new user into the database"""
        # Create a new user with email and password passed
        user = User(email=email, hashed_password=hashed_password)
        # Get session to communicate with the db
        session = self._session
        # Add user to database session
        session.add(user)
        # save changes to the database
        session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """
           Find a user by given key as a parameter
           Raise NoResultFound if user does not exist,
           Raise InvalidRequestError if user does not have the key.
        """
        keys = ['id', 'email', 'hashed_password', 'reset_token', 'session_id']
        for key, value in kwargs.items():
            if key not in keys:
                raise InvalidRequestError
        session = self._session
        all_users = session.query(User)
        user = all_users.filter_by(**kwargs).first()
        if user is None:
            raise NoResultFound

        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """
           Call find_user_id to locate the user to update.
           update the user's attributes as passed in the arguments.
           if an argument not valid for the object raise ValueError.
        """
        valid_attrs = [
                'id', 'email', 'hashed_password', 'reset_token', 'session_id']
        # Get user to update
        search_by = {'id': user_id}
        user = self.find_user_by(**search_by)
        # check if all arguments are valid for user object
        for key, value in kwargs.items():
            if key not in valid_attrs:
                raise ValueError
            setattr(user, key, value)
