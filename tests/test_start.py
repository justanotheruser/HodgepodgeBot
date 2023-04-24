from unittest.mock import AsyncMock
from aiogram.types import ReplyKeyboardRemove
import pytest

from denis_hodge_podge_bot.handlers.start import start


def get_answer_kwargs(mock):
    args, kwargs = mock.answer.call_args_list[0]
    assert len(args) == 0
    return kwargs


@pytest.mark.asyncio
async def test_start():
    command_mock = AsyncMock(command='start')
    await start(command_mock)
    kwargs = get_answer_kwargs(command_mock)
    assert '/weather' in kwargs['text']
    assert '/exchange' in kwargs['text']
    assert '/poll' in kwargs['text']
    assert '/cute_animal' in kwargs['text']
    assert kwargs['reply_markup'] == ReplyKeyboardRemove()
