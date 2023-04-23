from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove

router = Router()


@router.message(Command('start'))
async def start(message: Message):
    text = "Hello! I can help with some stuff. This is what I can do:\n" \
           "/weather - Get current weather in a city"
    await message.answer(text=text, reply_markup=ReplyKeyboardRemove())
