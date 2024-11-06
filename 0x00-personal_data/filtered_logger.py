#!/ust/bin/env python3
""" create a mysql connector"""
import os
import mysql.connector


def get_db():
    """Returns a connector to MySQL database server."""

    user = os.environ.get('PERSONAL_DATA_DB_USERNAME')
    passwd = os.environ.get('PERSONAL_DATA_DB_PASSWORD')
    host = os.environ.get('PERSONAL_DATA_DB_HOST')
    db_name = os.environ.get('PERSONAL_DATA_DB_NAME')

    # Create a database connection to MySQL server connect()
    db = mysql.connector.connect(
            database=db_name, host=host, user=user, passwd=passwd)

    return db
