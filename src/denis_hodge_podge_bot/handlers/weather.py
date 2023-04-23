import aiohttp
from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from denis_hodge_podge_bot.weather.weatherstock import get_weather

router = Router()


@router.message(Command(commands=['weather']))
async def weather(message: Message, command: CommandObject, aiohttp_session: aiohttp.ClientSession):
    if not command.args:
        await message.answer(text='Формат команды: /weather <Название Города>')
        return

    weather_data = await get_weather(aiohttp_session, message.text)
    text = f'__{weather_data.location}__\n' \
           f'_{weather_data.description}_\n' \
           f'*Температура*: {weather_data.temperature}\n' \
           f'*Влажность*: {weather_data.humidity}%\n' \
           f'*Скорость ветра*: {weather_data.wind_speed} км/ч\n'
    await message.answer(text=text, parse_mode='MarkdownV2')
