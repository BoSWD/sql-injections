import os
import sqlite3
import uuid

from server.utils import exception_pass


class Database:
    table_name = ""

    def __init__(self, db_path: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "db.sql")):
        self.db_path = db_path

    def __enter__(self):
        self.db_conn = sqlite3.connect(self.db_path)
        self.cursor = self.db_conn.cursor()
        return self

    def __exit__(self):
        self.db_conn.commit()
        self.db_conn.close()

    @exception_pass
    def filter_by(self, field, value):
        self.cursor.execute(f"SELECT * from {self.table_name} WHERE {field} = '{value}'")
        return self.cursor.fetchall()

    @exception_pass
    def find_one(self, field, value):
        self.cursor.execute(f"SELECT * from {self.table_name} WHERE {field} = '{value}'")
        return self.cursor.fetchone()

    @exception_pass
    def add(self, *values):
        add_values = f"INSERT INTO {self.table_name} VALUES ("
        for v in values:
            add_values += f"'{v}', "
        add_values = add_values[:len(add_values)-2] + ")"
        self.cursor.execute(add_values)

    def __del__(self):
        self.db_conn.close()


class User(Database):
    table_name = "users"

    @exception_pass
    def create_table(self):
        self.cursor.execute(
            f"""CREATE TABLE {self.table_name} (username text, password text, secret text)""")
        self.db_conn.commit()

    @exception_pass
    def find_user(self, username, password):
        self.cursor.execute(
            f"SELECT secret from {self.table_name} WHERE username = '{username}' and password = '{password}'")
        return self.cursor.fetchall()


def base_example(db_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), "db.sql")):
    if os.path.exists(db_path):
        os.remove(db_path)
    users = [
        {"username": "admin", "password": "uspertop", "mail": "admin_sql@gmail.ja", "superuser": 1},
        {"username": "Ivan", "password": "1234", "mail": "ivan1995@mail.com", "superuser": 0},
        {"username": "Betty", "password": "qwerty", "mail": "betty2000@mail.com", "superuser": 0}
    ]
    with User(db_path) as users_m:
        users_m.create_table()

        for user in users:
            users_m.add(str(uuid.uuid4()), user["username"], user["mail"], user["password"], user["superuser"])
