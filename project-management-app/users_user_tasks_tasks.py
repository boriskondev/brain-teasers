import sqlite3
from sqlite3 import Error

# =================================== NOTES ===================================
# One to many relationship between tables users - user_tasks - tasks is working well when adding new records.
# A good practice to be implemented in the main file - dividing the code into sections with comment headers.

# =================================== FUNCTIONS ===================================


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


def create_tasks_table(connection):
    create_table = """CREATE TABLE IF NOT EXISTS tasks (
      task_id INTEGER PRIMARY KEY AUTOINCREMENT, 
      task_name TEXT NOT NULL
    );
    """
    execute_query(connection, create_table)


def create_user_task_table(connection):
    create_table = """CREATE TABLE user_task (
        user_id INTEGER NOT NULL,
        task_id INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE RESTRICT ON UPDATE CASCADE,
        FOREIGN KEY (task_id) REFERENCES tasks (task_id) ON DELETE RESTRICT ON UPDATE CASCADE,
        PRIMARY KEY (user_id, task_id)
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


def add_task_to_tasks_table(connection, task_name):
    create_task = """
        INSERT INTO tasks (task_name)
        VALUES (?);
        """
    data = (task_name, )
    cursor = connection.cursor()
    cursor.execute(create_task, data)
    connection.commit()
    cursor.close()


def add_user_task_info(connection, user_id, task_id):
    create_user_task = """
        INSERT INTO user_task (user_id, task_id)
        VALUES (?, ?);
        """
    data = (user_id, task_id)
    cursor = connection.cursor()
    cursor.execute(create_user_task, data)
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


# =================================== MAIN LOGIC ===================================

db_connection = None

path = "app_db/many_to_many.sqlite"

try:
    db_connection = sqlite3.connect(path)
    print("Connection to SQLite DB successful")
except Error as e:
    print(f"The error \"{e}\" occurred")

create_users_table(db_connection)
create_tasks_table(db_connection)
create_user_task_table(db_connection)

# while True:
#     name_of_user = input("Name of the user: ")
#     if name_of_user == "N":
#         break
#     email_of_user = input("Email of the user: ")
#     department_of_user = input("Department of the user: ")
#     add_user_to_users_table(db_connection, name_of_user, email_of_user, department_of_user)
#
# while True:
#     name_of_task = input("Name of the task: ")
#     if name_of_task == "N":
#         break
#     add_task_to_tasks_table(db_connection, name_of_task)
#
# while True:
#     id_of_user = input("ID of the user: ")
#     if id_of_user == "N":
#         break
#     id_of_task = input("ID of the task: ")
#     add_user_task_info(db_connection, id_of_user, id_of_task)


# =================================== OUTPUT ===================================

select_users = """
SELECT * from users
"""

users = execute_read_query(db_connection, select_users)

print("ALL USERS:")
for user in users:
    print(user)

select_tasks = """
SELECT * from tasks
"""

tasks = execute_read_query(db_connection, select_tasks)

print("ALL TASKS:")
for task in tasks:
    print(task)

# select_user_tasks = """
# SELECT * from user_task
# """
#
# user_tasks = execute_read_query(db_connection, select_user_tasks)
#
# print("ALL USER TASKS:")
# for task in user_tasks:
#     print(task)

select = """
SELECT t.task_id, t.task_name, u.user_id, u.user_name 
FROM users u
INNER JOIN user_task ut
ON u.user_id = ut.user_id
INNER JOIN tasks t
ON ut.task_id = t.task_id;
"""

user_tasks = execute_read_query(db_connection, select)

print("ALL TASKS AND THEIR USERS:")
[print(user_task) for user_task in sorted(user_tasks, key=lambda x: x[0], reverse=False)]

# filtered = list(filter(lambda x: x[0] == 1, user_tasks))
#
# [print(x[3]) for x in filtered]