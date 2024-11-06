#!/usr/bin/env python3
""" a function to create a mysql server connector"""
import os
import mysql.connector


def get_db() -> mysql.connector.connection.MYSQLConnection:
    """Returns a connector to MySQL database server."""

    user = os.environ.get('PERSONAL_DATA_DB_USERNAME', 'root')
    passwd = os.environ.get('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.environ.get('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.environ.get('PERSONAL_DATA_DB_NAME')

    # Create a database connection and get connector to MySQL server connect()
    db = mysql.connector.connect(
            database=db_name, host=host, user=user, passwd=passwd)

    return db
