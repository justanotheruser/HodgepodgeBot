import logging

import aiohttp
from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from denis_hodge_podge_bot.weather.weatherstock import get_weather

router = Router()
logger = logging.getLogger('HodgepodgeBot')


@router.message(Command(commands=['weather']))
async def weather(message: Message, command: CommandObject, aiohttp_session: aiohttp.ClientSession):
    if not command.args:
        await message.answer(text='Формат команды: /weather <Название Города>')
        return

    try:
        weather_data = await get_weather(aiohttp_session, command.args)
    except Exception as e:
        logger.error(f"Error during getting weather data:\n exception: {type(e)}: {str(e)}\nmessage {message}")
        await message.answer(text="Упс! Что-то пошло не так. Попробуйте повторить запрос позже")
        return

    text = f'__{weather_data.location}__\n'
    if weather_data.description:
        text += f'_{weather_data.description}_\n'
    text += f'*Температура*: {weather_data.temperature}\n' \
            f'*Влажность*: {weather_data.humidity}%\n' \
            f'*Скорость ветра*: {weather_data.wind_speed} км/ч\n'
    await message.answer(text=text, parse_mode='MarkdownV2')
