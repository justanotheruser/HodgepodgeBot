import contextlib
import json
import logging
import os
import shutil
import tempfile

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from aiohttp import ClientSession

router = Router()
logger = logging.getLogger('HodgepodgeBot')


@router.message(Command(commands=['cute_animal']))
async def cute_animal(message: Message, aiohttp_session: ClientSession):
    async with aiohttp_session.get('https://dog.ceo/api/breeds/image/random') as response:
        json_data = json.loads(await response.text())
        async with aiohttp_session.get(json_data['message']) as photo_response:
            photo = await photo_response.read()
            with tempdir() as dirpath:
                with open('cute_animal.jpg', 'wb') as file:
                    file.write(photo)
                uploaded_image = FSInputFile(os.path.join(dirpath, 'cute_animal.jpg'))
                await message.answer_photo(uploaded_image)


@contextlib.contextmanager
def cd(newdir, cleanup=lambda: True):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)
        cleanup()


@contextlib.contextmanager
def tempdir():
    dirpath = tempfile.mkdtemp()

    def cleanup():
        shutil.rmtree(dirpath)

    with cd(dirpath, cleanup):
        yield dirpath
