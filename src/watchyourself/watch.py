import argparse
from datetime import datetime
from time import sleep
import subprocess
import os
from .util import get_cursor

os_name = os.uname().sysname


def active_process_and_window():
    if os_name == "Darwin":
        cmd = "osascript -e 'tell application \"System Events\" to tell (first process whose frontmost is true) to return {name, name of window 1}'" # noqa: E501
        output = subprocess.check_output(cmd, shell=True).decode(
            "utf-8").strip('\n').strip('{').strip('}').strip('\'')
        name, name_window = output.split(", ")
        return name, name_window
    elif os_name == "Linux":
        # TODO: Test on Linux
        cmd = "xdotool getactivewindow getwindowname"
        output = subprocess.check_output(cmd, shell=True).decode(
            "utf-8").strip('\n').strip('{').strip('}').strip('\'')
        name, name_window = output.split(", ")
        return name, name_window
    elif os_name == "Windows":
        try:
            import win32gui
            import win32process
            import psutil
        except ImportError:
            print("Please install pywin32")
            exit(1)
        window = win32gui.GetForegroundWindow()
        pid = win32process.GetWindowThreadProcessId(window)
        return (psutil.Process(pid[-1]).name(), win32gui.GetWindowText(window))
    else:
        raise ValueError("OS not supported, please use Linux, Mac or Windows")


def main(database: str = "watchyourself.db", table: str = "watch"):
    cursor, conn = get_cursor(database, table)
    while True:
        sleep(1)
        # get active process and window
        name, name_window = active_process_and_window()
        # get current time
        now = datetime.now()
        formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
        # save to database
        query = "INSERT INTO {} VALUES (?, ?, ?, ?)".format(table)
        cursor.execute(query, (name, name_window, formatted_time, None))
        conn.commit()
        # not use this 
        # cursor.execute(f"INSERT INTO {table} VALUES (?, ?, ?, ?)", (name, name_window, now, None))  # noqa: E501
        print(f"now: {now}, Name: {name}, Window: {name_window}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, default="config.yaml")
    parser.add_argument("--database", type=str, default="watchyourself.db")
    parser.add_argument("--table", type=str, default="watch")
    args = parser.parse_args()
    main(args.database, args.table)
