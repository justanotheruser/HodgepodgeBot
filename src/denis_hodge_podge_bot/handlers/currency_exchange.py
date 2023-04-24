import aiohttp
from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from denis_hodge_podge_bot.currency_exchange import currency_code_converter
from denis_hodge_podge_bot.currency_exchange import split_value_source_target
from denis_hodge_podge_bot.currency_exchange.exchange_rates_data import convert

router = Router()


@router.message(Command(commands=['exchange']))
async def exchange(message: Message, command: CommandObject, aiohttp_session: aiohttp.ClientSession):
    if not command.args:
        # TODO: auto-generate random (but valid) example
        helper_text = 'Формат команды: /exchange <кол-во> <валюта> в <валюте>\n' \
                      'Например: /exchange 200,5 долларов в датских кронах'
        await message.answer(text=helper_text)
        return

    value, source_currency, target_currency = split_value_source_target(command.args)
    source_currency_code = currency_code_converter.identify_source_currency(source_currency)
    target_currency_code = currency_code_converter.identify_target_currency(target_currency)
    result_value = await convert(aiohttp_session, value, source_currency_code, target_currency_code)
    result_value = str(round(result_value, 2))
    await message.answer(text=result_value)
