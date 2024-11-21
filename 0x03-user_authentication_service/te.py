#!/usr/bin/env python3

from auth import Auth
from user import User
from db import DB

AUTH = Auth()
email = 'bob@bob.com'
password = 'MyPwdOfBob'

user = AUTH.register_user(email, password)
print(AUTH.get_reset_password_token(email))
print(user.reset_token)
fake_email = "dan2@dan.com"
try:
    print(AUTH.get_reset_password_token(fake_email))
except ValueError:
    print('fuck exception')

AUTH.update_password(reset_token=user.reset_token, password='123')
print(user.reset_token)
print(user.hashed_password)
