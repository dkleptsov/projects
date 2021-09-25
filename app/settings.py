import os


# telegram bot settings
ADMIN_ID = 1631744908
LOGS_PATH = "app/task_bot.log"
BOT_TOKEN = os.getenv("TASK_BOT")

START_MSG = "Task scheduling started automatically!"


# task db settings
TASKS_DB_PATH = "app/tasks_db/tasks.db"
TASKS_DB_TEST_PATH = "app/tasks_db/tasks_test.db"


# test settings
TEST_TASK_LIST_1 = ['*0*', '*1*', '*2*', '*3*', '*4*']
TEST_TASK_LIST_2 = ['*A*','*B*','*C*']