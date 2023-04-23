import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import config

logger = logging.getLogger(__name__)


async def main():
    dp = Dispatcher(storage=MemoryStorage())
    bot = Bot(token=config.bot_token.get_secret_value())
    await dp.start_polling(bot)


def cli():
    """Wrapper for command line"""
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")


if __name__ == '__main__':
    cli()
