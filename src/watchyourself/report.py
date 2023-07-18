import argparse
from .util import get_cursor, get_inspects


def main(database: str = "watchyourself.db", table: str = "watch"):
    cursor, _ = get_cursor(database, table)
    inspect_objects = get_inspects(cursor, table)
    for inspect_object in inspect_objects:
        print(inspect_object)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, default="config.yaml")
    parser.add_argument("--database", type=str, default="watchyourself.db")
    parser.add_argument("--table", type=str, default="watch")
    args = parser.parse_args()
    main(args.database, args.table)
