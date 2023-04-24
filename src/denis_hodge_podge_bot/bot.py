import asyncio
import logging

import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import config
from handlers import start, weather, currency_exchange, poll
from middlewares.add_aiohttp_session import AddAiohttpSessionMiddleware

logger = logging.getLogger('HodgepodgeBot')


async def main():
    logger.setLevel(logging.INFO)
    setup_console_logger(logger)

    dp = Dispatcher(storage=MemoryStorage())
    bot = Bot(token=config.bot_token.get_secret_value())

    dp.include_router(start.router)
    dp.include_router(weather.router)
    dp.include_router(currency_exchange.router)
    dp.include_router(poll.router)
    async with aiohttp.ClientSession() as session:
        dp.update.middleware(AddAiohttpSessionMiddleware(session))
        await dp.start_polling(bot)


def cli():
    """Wrapper for command line"""
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")


def setup_console_logger(logger):
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    ch.setFormatter(ch_formatter)
    logger.addHandler(ch)


if __name__ == '__main__':
    cli()
