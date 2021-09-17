import asyncio
from loguru import logger
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import app.settings
from app.handlers.tasks import register_handlers_tasks


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/add_task", description="Add new task."),
        BotCommand(command="/perform_task", description="Perform task."),
        BotCommand(command="/cancel", description="Cancel current operation."),
    ]
    await bot.set_my_commands(commands)


async def main():
    logger.add(app.settings.LOGS_PATH, rotation="10 MB")
    bot = Bot(token=app.settings.BOT_TOKEN)
    dp = Dispatcher(bot, storage=MemoryStorage())
    register_handlers_tasks(dp, app.settings.ADMIN_ID)
    await set_commands(bot)
    logger.info("Task bot bot started!")    
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
