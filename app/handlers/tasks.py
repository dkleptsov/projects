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


def register_handlers_tasks(dp: Dispatcher, admin_id: int):
    """ This is needed to catch commands from user. """
    dp.register_message_handler(cmd_cancel,
                                IDFilter(user_id=admin_id),
                                commands="cancel",
                                state="*")

    dp.register_message_handler(new_task, 
                                IDFilter(user_id=admin_id), 
                                commands="add_task")
    dp.register_message_handler(enter_task_description,
                                IDFilter(user_id=admin_id),
                                state=AddTask.task_description)

    dp.register_message_handler(perform_task,
                                IDFilter(user_id=admin_id),
                                commands="perform_task")    
    dp.register_message_handler(choose_task,
                                IDFilter(user_id=admin_id),
                                state=PerformTask.choose_task)
    dp.register_message_handler(enter_results,
                                IDFilter(user_id=admin_id),
                                state=PerformTask.enter_results)

    app.tasks_db.actions.init_db()

async def cmd_cancel(message: types.Message, state: FSMContext):
    """ This cancel any current operation. """
    await state.finish()
    await message.answer("Action is canceled.", 
                         reply_markup=types.ReplyKeyboardRemove())


async def new_task(message: types.Message, state: FSMContext):
    """ Sets state so user can enter task description. """
    await message.answer("Enter description of the task.",
                         reply_markup=types.ReplyKeyboardRemove())
    await AddTask.task_description.set()


async def enter_task_description(message: types.Message, state: FSMContext):
    """ Adds new task to database. """
    app.tasks_db.actions.add_task(message["text"], message["from"]["id"])
    await message.answer(f"Task {message['text']} added successfuly!",
                         reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


async def perform_task(message: types.Message, state: FSMContext):
    """ Sends list of tasks and sets state so user can choose task. """
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard.add(*app.tasks_db.actions.get_unfinished_tasks(message["from"]["id"]))
    await message.answer("Choose task:", reply_markup=keyboard)
    await PerformTask.choose_task.set()


async def choose_task(message: types.Message, state: FSMContext):
    """ Starts timer of a task. Sets state so user can enter result. """
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Done!", "Failed")
    await message.answer(f"Task {message['text']} is chosen!", 
                         reply_markup=keyboard)
    app.tasks_db.actions.begin_task(message['text'], message["from"]["id"])
    await PerformTask.enter_results.set()
    

async def enter_results(message: types.Message, state: FSMContext):
    """ Logs if task is completed and logs spent hours. """
    if message['text'] == "Done!":
        await message.answer(app.tasks_db.actions.complete_task(message["from"]["id"]))
        await message.answer("DOOOOONE",
                             reply_markup=types.ReplyKeyboardRemove())
    elif message['text'] == "Failed":
        await message.answer(app.tasks_db.actions.add_time(message["from"]["id"]))
        await message.answer("FAILED",
                             reply_markup=types.ReplyKeyboardRemove())
    await state.finish()
