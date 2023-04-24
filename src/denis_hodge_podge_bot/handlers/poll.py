import logging

from aiogram import Router, F
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from denis_hodge_podge_bot.config import config
from denis_hodge_podge_bot.keyboards.yes_or_no_keyboard import get_yes_or_no_keyboard

router = Router()
logger = logging.getLogger('HodgepodgeBot')


class CreatePoll(StatesGroup):
    adding_options = State()
    choosing_privacy = State()


@router.message(Command(commands=['poll']))
async def create_poll(message: Message, command: CommandObject, state: FSMContext):
    if not command.args:
        await message.answer(text='Формат команды: /poll <Текст вопроса>')
        return

    await state.update_data(poll_question=command.args)
    await message.answer(
        text="Добавьте вариант ответа (/done чтобы закончить, /cancel - отменить создание опроса)"
    )
    await state.set_state(CreatePoll.adding_options)


@router.message(CreatePoll.adding_options, Command(commands=['cancel']))
async def cancel_poll(message: Message, state: FSMContext):
    await message.answer(text='Создание опроса отменено')
    await state.clear()


@router.message(CreatePoll.adding_options, Command(commands=['done']))
async def options_are_chosen(message: Message, state: FSMContext):
    user_data = await state.get_data()
    if 'poll_options' not in user_data or len(user_data['poll_options']) < 2:
        await message.answer(text='Добавьте хотя бы два варианта ответа')
        return
    await message.answer(text=f'Варианты ответов: {user_data["poll_options"]}\n'
                              f'Будет ли этот опрос анонимным?',
                         reply_markup=get_yes_or_no_keyboard('Будет ли опрос анонимным?'))
    await state.set_state(CreatePoll.choosing_privacy)


@router.message(CreatePoll.adding_options, F.text)
async def add_option(message: Message, state: FSMContext):
    user_data = await state.get_data()
    if 'poll_options' not in user_data:
        user_data['poll_options'] = [message.text]
    else:
        user_data['poll_options'].append(message.text)
    await state.update_data(poll_options=user_data['poll_options'])


@router.message(CreatePoll.choosing_privacy, F.text.in_(['Да', 'Нет']))
async def chosen_privacy_settings(message: Message, state: FSMContext):
    user_data = await state.get_data()
    user_data['is_anonymous'] = True if message.text == 'Да' else False
    await state.bot.send_poll(chat_id=config.polls_group_chat_id, question=user_data['poll_question'],
                              options=user_data['poll_options'], is_anonymous=user_data['is_anonymous'])
    await state.clear()
    await message.answer(text="Опрос создан успешно!", reply_markup=ReplyKeyboardRemove())
