import sqlite3
from sqlite3 import Error


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


def create_users_table(connection):
    create_table = """CREATE TABLE IF NOT EXISTS users (
      user_id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_name TEXT NOT NULL,
      email TEXT NOT NULL,
      department TEXT NOT NULL
    );
    """

    execute_query(connection, create_table)


def add_user_to_users_table(connection, user_name, user_email, user_department):
    create_user = """
        INSERT INTO users (user_name, email, department)
        VALUES (?, ?, ?);
        """
    data = (user_name, user_email, user_department)
    cursor = connection.cursor()
    cursor.execute(create_user, data)
    connection.commit()
    cursor.close()


def create_clients_table(connection):
    create_table = """CREATE TABLE IF NOT EXISTS clients (
      client_id INTEGER PRIMARY KEY AUTOINCREMENT,
      client_name TEXT NOT NULL,
      created_by INTEGER NOT NULL,
      FOREIGN KEY (created_by) REFERENCES users (user_id)
    );
    """
    execute_query(connection, create_table)


def add_client_to_clients_table(connection, client_name, user_id):
    create_client = """
        INSERT INTO clients (client_name, created_by)
        VALUES (?, ?);
        """
    data = (client_name, user_id)
    cursor = connection.cursor()
    cursor.execute(create_client, data)
    connection.commit()
    cursor.close()


def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


db_connection = None

path = "app_db/db.sqlite"

try:
    db_connection = sqlite3.connect(path)
    print("Connection to SQLite DB successful")
except Error as e:
    print(f"The error \"{e}\" occurred")

create_users_table(db_connection)
create_clients_table(db_connection)

while True:
    name_of_user = input("Name of the user: ")
    if name_of_user == "N":
        break
    email_of_user = input("Email of the user: ")
    department_of_user = input("Department of the user: ")
    add_user_to_users_table(db_connection, name_of_user, email_of_user, department_of_user)

while True:
    try:
        user_to_add = input("For which user do you want to add a client? ")
        if user_to_add == "N":
            break
        select_users = f"""
        SELECT user_id from users
        WHERE user_name == "{user_to_add}"
        """

        id_of_user = execute_read_query(db_connection, select_users)[0][0]
        name_of_client = input("What is the name of the client? ")

        add_client_to_clients_table(db_connection, name_of_client, id_of_user)

    except Error as e:
        print(f"The error '{e}' occurred")


select_users = """
SELECT * from users
"""

users = execute_read_query(db_connection, select_users)

print("ALL USERS:")
for user in users:
    print(user)

select_clients = """
SELECT * from clients
"""

clients = execute_read_query(db_connection, select_clients)

print("ALL CLIENTS:")
for client in clients:
    print(client)


# SELECT DATA FOR USERS AND CLIENTS (TWO TABLES)
#
# select_clients_per_user = """
# SELECT user_id, user_name, client_id, client_name FROM users INNER JOIN clients ON clients.created_by = users.user_id
# """
#
# users = execute_read_query(db_connection, select_clients_per_user)
#
# for user in users:
#     print(user)

# DELETE USER
#
# delete_user = """
# DELETE from users WHERE user_name == "Mitko"
# """
#
# execute_query(connection, delete_user)

# SELECT USER
# select_users = """
# SELECT * from users
# """
#
# users = execute_read_query(db_connection, select_users)
#
# for user in users:
#     print(user)