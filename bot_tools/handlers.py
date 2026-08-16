from aiogram import Router, F
from aiogram.types import Message, voice, user

from db import Users
from generate_text import generate_response_text


db = Users()


db.init_db()

router = Router()


@router.message(F.text)
async def text_input(message: Message):
    user_id = message.from_user.id
    name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = message.from_user.username


    prompt = message.text

    db.add_user(user_id, name, last_name, username)




    if prompt == '/clean':
        db.clean_history(user_id)
        await message.answer(text='я все забыл')


    else:
        response = generate_response_text(user_id, prompt)


        await message.answer(text=response)





@router.message(F.voice)
async def voice_input(message: Message):
    pass