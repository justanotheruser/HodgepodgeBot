from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove

router = Router()


@router.message(Command(commands=['start']))
async def start(message: Message):
    text = "Привет! Я бот, умеющий делать разные штуки. Например:\n" \
           "/weather - Получить текущую погоду в городе\n" \
           "/exchange - Конвертация валют по текущему курсу\n" \
           "/poll - Создать новый опрос и отправить его в групповой чат\n" \
           "/cute_animal - Прислать фото милого животного"
    await message.answer(text=text, reply_markup=ReplyKeyboardRemove())
