from typing import Optional

from aiogram import types


def get_yes_or_no_keyboard(input_placeholder: Optional[str] = None):
    kb = [
        [
            types.KeyboardButton(text="Да"),
            types.KeyboardButton(text="Нет")
        ],
    ]
    return types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder=input_placeholder
    )
