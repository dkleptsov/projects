from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, IDFilter
from aiogram.dispatcher.filters.state import State, StatesGroup


TASKS = ["Run 5km or more and do strength training.", 
         "Website, presentations and bots on DL (2 hours).", 
         "Programming (2 hours)."]
TASK1_MSG = "Good morning! \nTask1: Run 5km or more and do strength training."
TASK2_MSG = "Task2: Website, presentations and bots on DL (2 hours)."
TASK3_MSG = "Task3: Programming (2 hours)."

task_status = ["Done!", "Failed"]

keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
keyboard.add(*task_status)


class MorningTasks(StatesGroup):
    waiting_task1 = State()
    waiting_task2 = State()
    waiting_task3 = State()
    waiting_task4 = State()
    

# state types: 'start', 'next', 'finish'

# async def xxx(**kwargs): #message: types.Message, state: FSMContext, state_type: str):
#     for kwarg in kwargs:
#         print(kwarg)
#     # First element of check-list
#     # if state_type == 'start':
#     #     await message.answer(TASK1_MSG, reply_markup=keyboard)
#     #     await MorningTasks.waiting_task1.set()
        
                
    # if message.text not in task_status:
    #     await message.answer("Please use provided buttons")
    #     return
    # await state.update_data(task1_result=message.text)
    # await message.answer(TASK2_MSG, reply_markup=keyboard)
    # await MorningTasks.next() # для простых шагов можно обходится next()


  
    
async def morning_start(message: types.Message, state: FSMContext):
    await message.answer(TASK1_MSG, reply_markup=keyboard)
    await MorningTasks.waiting_task1.set()


async def task1_result(message: types.Message, state: FSMContext):
    if message.text not in task_status:
        await message.answer("Please use provided buttons")
        return
    await state.update_data(task1_result=message.text)
    await message.answer(TASK2_MSG, reply_markup=keyboard)
    await MorningTasks.next() # для простых шагов можно обходится next()


async def task2_result(message: types.Message, state: FSMContext):
    if message.text not in task_status:
        await message.answer("Please use provided buttons")
        return
    await state.update_data(task2_result=message.text)
    await message.answer(TASK2_MSG, reply_markup=keyboard)    
    await MorningTasks.next() # для простых шагов можно обходится next()


async def task3_result(message: types.Message, state: FSMContext):
    if message.text not in task_status:
        await message.answer("Please use provided buttons")
        return
    await state.update_data(task3_result=message.text)
    user_data = await state.get_data()
    await message.answer(f"Task 1 result: {user_data['task1_result']}\n"\
                         f"Task 2 result: {user_data['task2_result']}\n"\
                         f"Task 3 result: {user_data['task3_result']}\n",
                         reply_markup=types.ReplyKeyboardRemove())
    await state.finish()



def register_handlers_morning(dp: Dispatcher, admin_id: int):
    dp.register_message_handler(morning_start, 
                IDFilter(user_id=admin_id), commands="morning", state="*")
    dp.register_message_handler(task1_result, 
                                state=MorningTasks.waiting_task1)
    dp.register_message_handler(task2_result, 
                                state=MorningTasks.waiting_task2)
    dp.register_message_handler(task3_result, 
                                state=MorningTasks.waiting_task3)


# TODO: Написать одну функцию для всех случаев
# TODO: Вынести данные отдельно
# TODO: Предусмотреть случай произвольной длины!