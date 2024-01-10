import os
import psycopg2
# from psycopg2.errors import DivisionByZero
from dotenv import load_dotenv
import database

MENU_PROMPT = """---MENU---

1) Add password
2) select a password by id 
3) update or delete a password

Enter your choice: """

DATABASE_PROMPT = "Enter the DATABASE_URL value or leave empty to load from.env file"


def prompt_create_user(connection, username, password):
    database.add_user(connection, username, password)


def prompt_delete_all_users(connection):
    database.delete_all_users(connection)


def prompt_delete_user(connection, _id):
    database.delete_user(connection, _id)


def prompt_login(connection):
    while True:
        username = input("Enter your username(enter 1 for adding a new user): ")
        if int(username) == 1:
            username = prompt_create_user(connection)
            return username
        password = input("Enter your main password: ")
        try:
            user_password = database.get_user(connection, username)[2]
            if user_password == password:
                return username
            else:
                print("password is wrong")
        except TypeError:
            print("no available user with this username")



def prompt_add_password(connection):
    pass

# MENU_OPTIONS = {
#     "1": prompt_add_password,
#     "2": prompt_select_password,
#     "3": prompt_update_password,
# }


def prompt_show_users(connection):
    users = database.get_users(connection)
    return users


def menu():

    database_url = input(DATABASE_PROMPT)
    if not database_url:
        load_dotenv()
        database_url = os.environ["DATABASE_URL"]

    connection = psycopg2.connect(database_url)
    database.create_tables(connection)
    username = prompt_login(connection)
    print(f"Hello {username}")
    while(selection := input(MENU_PROMPT)) != "0":
        try:
            MENU_OPTIONS[selection](connection)
        except KeyError:
            print("Invalid input selected, please try again.")

