from datetime import datetime
import os
import sqlite3


class Inspect:
    name: str
    window: str
    time: datetime
    category: str

    def __init__(self, name: str, window: str, time: datetime, category: str = None):
        self.name = name
        self.window = window
        self.time = time
        self.category = category

    def __str__(self):
        return f"{self.time}: {self.name} ... {self.window}"


def get_cursor(database: str, table: str):
    # get file path
    database = os.path.join(os.path.dirname(__file__), database)
    # if database does not exist, create it
    if not os.path.exists(database):
        conn = sqlite3.connect(database)
        c = conn.cursor()
        c.execute(f"CREATE TABLE {table} (name text, window text, time text, category text)")  # noqa: E501
        conn.commit()
        conn.close()
    # connect to database
    conn = sqlite3.connect(database)
    c = conn.cursor()
    # if table does not exist, create it
    c.execute(f"SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{table}'")  # noqa: E501
    if c.fetchone()[0] != 1:
        c.execute(f"CREATE TABLE {table} (name text, window text, time text, category text)")  # noqa: E501
        conn.commit()
    return c, conn


def get_inspects(cursor, table):
    cursor.execute(f"SELECT * FROM {table}")
    data = cursor.fetchall()
    inspect_objects = []
    for row in data:
        name = row[0]
        window = row[1]
        time = datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S")
        category = row[3]
        inspect_object = Inspect(name, window, time, category)
        inspect_objects.append(inspect_object)
    return inspect_objects
