from psycopg2.extras import execute_values

CREATE_USERS = '''CREATE TABLE IF NOT EXISTS users2
(id SERIAL PRIMARY KEY, username TEXT, main_password TEXT, app_id INTEGER);'''

CREATE_USERS2 = '''CREATE TABLE IF NOT EXISTS users2
(id SERIAL PRIMARY KEY, username TEXT, main_password TEXT, app_id INTEGER);'''

CREATE_PASSWORDS = '''CREATE TABLE IF NOT EXISTS passwords
(id SERIAL PRIMARY KEY, password_text TEXT,details TEXT, user_id INTEGER, FOREIGN KEY(user_id) REFERENCES users(id));'''

INSERT_USER = "INSERT INTO users (username, main_password) VALUES (%s, %s)"
SELECT_ALL_USERS = "SELECT * FROM users"
SELECT_USER = "SELECT * FROM users WHERE %s = %s"
SELECT_LAST_USER = "SELECT * FROM users ORDER BY id DESC LIMIT 1"
DELETE_ALL_USERS = "DELETE FROM users"
DELETE_USER = "DELETE FROM users WHERE id = %s"


def create_tables(connection):

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_USERS2)
            cursor.execute(CREATE_PASSWORDS)

def add_user(connection, username, main_password):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_USER, (username, main_password))


def get_users(connection):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ALL_USERS)
            return cursor.fetchall()


def get_user(connection, subject, item):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_USER, (subject, item))
            return cursor.fetchone()


def get_last_user(connection):

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_LAST_USER)
            return cursor.fetchone()


def delete_all_users(connection):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(DELETE_ALL_USERS)


def delete_user(connection, _id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(DELETE_USER, (_id,))