import psycopg2
from psycopg2.errors import InFailedSqlTransaction

connection = psycopg2.connect(dbname='telegrambot', user='postgres', password='1')
cur = connection.cursor()


def create_table_users():
    cur.execute("""DROP TABLE IF EXISTS users""")
    cur.execute("""
                 CREATE TABLE IF NOT EXISTS users
                (
                    user_id integer NOT NULL,
                    first_name varchar(100) NOT NULL,
                    last_name varchar(100),
                    email varchar(100) NOT NULL,
                    password varchar(100) NOT NULL,
                    CONSTRAINT PK_users_user_id PRIMARY KEY(user_id)
                
                )
                """)

    connection.commit()


def insert_user_in_db(user_id, first_name, last_name, email, password):
    cur.execute("""
                INSERT INTO users VALUES
                (%s,%s,%s,%s,%s)
                """, (user_id, first_name, last_name, email, password))
    connection.commit()


def select_user_from_db(user_id, email, password):
    try:
        cur.execute("""SELECT email, password FROM users WHERE user_id = %s and email = %s and password = %s""",
                    (user_id, email, password))
        connection.commit()
        full_fetch = cur.fetchall()
        return True if full_fetch else False
    except InFailedSqlTransaction:
        connection.rollback()


create_table_users()
