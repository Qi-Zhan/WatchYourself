import argparse
from util import get_cursor, Inspect
from datetime import datetime


def main(database: str, table: str):
    cursor, _ = get_cursor(database, table)
    # get all the data
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, default="config.yaml")
    parser.add_argument("--database", type=str, default="watchyourself.db")
    parser.add_argument("--table", type=str, default="watch")
    args = parser.parse_args()
    main(args.database, args.table)
