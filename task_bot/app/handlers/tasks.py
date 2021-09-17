import time
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, IDFilter
from aiogram.dispatcher.filters.state import State, StatesGroup
import app.tasks_db.actions


class AddTask(StatesGroup):
    task_description = State()


class PerformTask(StatesGroup):
    choose_task = State()
    enter_results = State()


task_status = ["Done!", "Failed"]

keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
keyboard.add(*task_status)


def register_handlers_tasks(dp: Dispatcher, admin_id: int):
    dp.register_message_handler(cmd_cancel, IDFilter(user_id=admin_id), commands="cancel", state="*")

    dp.register_message_handler(new_task, IDFilter(user_id=admin_id), commands="add_task")
    dp.register_message_handler(enter_task_description, IDFilter(user_id=admin_id), state=AddTask.task_description)

    dp.register_message_handler(perform_task, IDFilter(user_id=admin_id), commands="perform_task")    
    dp.register_message_handler(choose_task, IDFilter(user_id=admin_id), state=PerformTask.choose_task)
    dp.register_message_handler(enter_results, IDFilter(user_id=admin_id), state=PerformTask.enter_results)


async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Action is canceled.")


async def new_task(message: types.Message, state: FSMContext):
    await AddTask.task_description.set()
    await message.answer("Enter description of the task.")# SEND SHOULD BE SMART


async def enter_task_description(message: types.Message, state: FSMContext):
    """ Process new task description """
    app.tasks_db.actions.add_task(message["text"])
    await state.finish()
    await message.answer(f"Task {message['text']} added successfuly!")


async def perform_task(message: types.Message, state: FSMContext):
    await PerformTask.choose_task.set()
    await message.answer(app.tasks_db.actions.format_tasks())


async def choose_task(message: types.Message, state: FSMContext):
    await message.answer(f"Task {message['text']} is chosen!", reply_markup=keyboard)
    start = time.monotonic()

    await PerformTask.enter_results.set()
    

async def enter_results(message: types.Message, state: FSMContext):
    # Записать потраченные часы
    # if else удалять из базы или нет
    if message['text'] == "Done!":
        await message.answer("DOOOOONE")
    elif message['text'] == "Failed":
        await message.answer("FAILED")


