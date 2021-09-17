import os
import sqlite3
import sys


def create_tasks_db(db_path:str="app/tasks_db/tasks.db") -> None:
    """ Creates empty task db """
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("""CREATE TABLE tasks (
            user integer,
            task_name text,
            date_completed text,
            hours_spent real,
            task_group text,
            deadline text
            )""")
    conn.close()


def create_temp_db(db_path:str="app/tasks_db/tasks.db") -> None:
    """ Creates empty temp db """
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("""CREATE TABLE temp (
            started_time integer
            )""")
    conn.close()


def add_task(task_name:str, db_path:str="app/tasks_db/tasks.db") -> None:
    """ Adds task to a text file. """
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    with conn:
        c.execute(""" INSERT INTO tasks VALUES (:user, 
        :task_name, :date_completed, :hours_spent, :task_group, :deadline)""", 
            {"user": 1631744908,
             "task_name": task_name, 
             "date_completed": "", 
             "hours_spent": 0, 
             "task_group": "",
             "deadline": ""})
    conn.close()


def delete_task(task_to_delete:str, db_path:str="app/tasks_db/tasks.db") -> None:
    """ Deletes given task from text file.
        Returns True if deletion is successful. """
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    with conn:
        c.execute("DELETE from tasks WHERE task_name = :task_name",
                  {'task_name': task_to_delete})
    conn.close()


def load_tasks(db_path:str="app/tasks_db/tasks.db") -> list:
    """ Returns list of tasks in human readable form. 
        Strips from blanc symbols and lines. """
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    with conn:
        c.execute("SELECT * FROM tasks")
    return c.fetchall()


def modify_task(old_task:str, new_task:str, 
                db_path:str="app/tasks_db/tasks.db") -> None:
    """ Modify task if old task exists. """
    if delete_task(old_task, db_path=db_path):
        add_task(new_task, db_path=db_path)


def format_tasks(db_path:str="app/tasks_db/tasks.db"):
    task_list = load_tasks(db_path)
    output_str = "Choose task to perform:\n\n"
    for i, task in enumerate(task_list):
        output_str += f"[{i}] {task[1]}\n"
    return output_str


def main():
    # create_tasks_db()
    # create_temp_db()
    add_task("THIS IS TEST")
    print(load_tasks())
    delete_task("THIS IS TEST")
    delete_task("FIRST TASK")
    print(load_tasks())



    # for i in range(5):
    #     add_task(f" *{i}* ")
    # modify_task("*K*", "*F*")
    # print(load_tasks())


if __name__ == "__main__":
    main()
