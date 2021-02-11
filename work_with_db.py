#!/usr/bin/python3
import psycopg2
from psycopg2.errors import InFailedSqlTransaction

from config import PG_USER, PG_PASS

connection = psycopg2.connect(dbname='telegrambot', user=PG_USER, password=PG_PASS)
cur = connection.cursor()


def create_table_users():
    cur.execute("""
                 CREATE TABLE IF NOT EXISTS users
                (
                    id serial,
                    user_id integer NOT NULL,
                    first_name varchar(100) NOT NULL,
                    last_name varchar(100),
                    email varchar(100) NOT NULL,
                    password varchar(100) NOT NULL,
                    mail_activated bool default False NOT NULL,
                    user_authorization bool default False NOT NULL,
                    CONSTRAINT PK_users_id PRIMARY KEY(id) 
                )
                """)

    connection.commit()


def insert_user_in_db(user_id, first_name, last_name, email, password):
    cur.execute("""
                INSERT INTO users (user_id, first_name, last_name, email, password) 
                VALUES (%s,%s,%s,%s,%s)
                """, (user_id, first_name, last_name, email, password))
    connection.commit()


def select_user_from_db(user_id, email, password):
    try:
        cur.execute("""SELECT email, password FROM users WHERE user_id = %s and email = %s and password = %s""",
                    (user_id, email, password))
        connection.commit()
        fetch = cur.fetchall()
        return True if fetch else False
    except InFailedSqlTransaction:
        connection.rollback()


def select_user_account(user_id):
    try:
        cur.execute("""SELECT user_id FROM users WHERE user_id = %s""",
                    (user_id,))
        connection.commit()
        fetch = cur.fetchone()
        return True if fetch else False
    except InFailedSqlTransaction:
        connection.rollback()


def select_active_from_db(user_id):
    try:
        cur.execute("""SELECT mail_activated FROM users WHERE user_id = %s""",
                    (user_id,))
        connection.commit()
        fetch = cur.fetchone()
        if fetch:
            for result in fetch: ...
            return True if result else False
        else:
            return True if fetch else False
    except InFailedSqlTransaction:
        connection.rollback()


def select_auth_user(user_id):
    try:
        cur.execute("""SELECT user_authorization FROM users WHERE user_id = %s""",
                    (user_id,))
        connection.commit()
        fetch = cur.fetchone()
        if fetch:
            for result in fetch: ...
            return True if result else False
        else:
            return True if fetch else False
    except InFailedSqlTransaction:
        connection.rollback()


def update_mail_activated(email):
    cur.execute("""UPDATE users SET mail_activated = TRUE WHERE email = %s""",
                (email,))
    connection.commit()


def update_user_authorization(user_id):
    cur.execute("""UPDATE users SET user_authorization = TRUE WHERE mail_activated = TRUE and user_id = %s""",
                (user_id,))
    connection.commit()


create_table_users()
