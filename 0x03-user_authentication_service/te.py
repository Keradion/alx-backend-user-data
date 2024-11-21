#!/usr/bin/env python3

from auth import Auth
from user import User
from db import DB

auth = Auth()
email = 'bob@bob.com'
password = 'MyPwdOfBob'

auth.register_user(email, password)

print(auth.get_reset_password_token(email))

fake_email = "dan2@dan.com"
try:
    print(auth.get_reset_password_token(fake_email))
except ValueError:
    print('fuck exception')
