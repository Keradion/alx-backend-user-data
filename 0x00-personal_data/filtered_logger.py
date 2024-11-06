#!/usr/bin/env python3
""" a function to create a mysql server connector"""
import os
import re
import mysql.connector
from typing import List


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str
        ) -> str:
    """ Return obfuscated log message """
    for key in fields:
        message = re.sub(rf"{key}=[^;]*", f"{key}={redaction}", message)

    return message


def get_db() -> "MySQL Connector":
    """Returns a connector to MySQL database server."""

    user = os.environ.get('PERSONAL_DATA_DB_USERNAME', 'root')
    passwd = os.environ.get('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.environ.get('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.environ.get('PERSONAL_DATA_DB_NAME')

    # Create a database connection and get connector to MySQL server connect()
    db = mysql.connector.connect(
            database=db_name, host=host, user=user, passwd=passwd)

    return db
