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
      email TEXT,
      department TEXT
    );
    """

    execute_query(connection, create_table)


def create_clients_table(connection):
    create_table = """CREATE TABLE IF NOT EXISTS clients (
      client_id INTEGER PRIMARY KEY AUTOINCREMENT,
      client_name TEXT NOT NULL,
      created_by INTEGER NOT NULL,
      FOREIGN KEY (created_by) REFERENCES users (user_id)
    );
    """
    execute_query(connection, create_table)


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

select_clients_per_user = """
SELECT user_id, user_name, client_id, client_name FROM users INNER JOIN clients ON clients.created_by = users.user_id
"""

users = execute_read_query(db_connection, select_clients_per_user)

for user in users:
    print(user)
