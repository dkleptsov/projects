import os
import asyncio
from loguru import logger
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from app.handlers.tasks import register_handlers_tasks


async def set_commands(bot: Bot):
    """ Telegram will show this hints when / is pressed. """
    commands = [
        BotCommand(command="/add_task", description="Add new task."),
        BotCommand(command="/perform_task", description="Perform task."),
        BotCommand(command="/cancel", description="Cancel current operation."),
    ]
    await bot.set_my_commands(commands)


async def main():
    """ Main loop of the bot. """
    logger.add("data/bot.log", rotation="10 MB")
    logger.info("Task bot bot started!")

    bot = Bot(token=os.getenv("TASK_BOT"))
    dp = Dispatcher(bot, storage=MemoryStorage())
    register_handlers_tasks(dp, os.getenv("ADMIN_ID"))
    await set_commands(bot)  
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
