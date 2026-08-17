from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import Message, voice, user

from db import Users
from generate_text import generate_response_text
from convertor import convert_ogg_to_wav
from audio_recognation import voice_to_text



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
    user_id = message.from_user.id

    file_id = message.voice.file_id


    await message.bot.download(
        message.voice,
        destination=f"audio/{user_id}_{file_id}.ogg"
    )


    convert_ogg_to_wav(f"audio/{user_id}_{file_id}.ogg", f"audio/{user_id}_{file_id}.wav")

    prompt = voice_to_text(f"audio/{user_id}_{file_id}.wav")
    print(prompt)


    response = generate_response_text(user_id, prompt)

    await message.answer(text=response, parse_mode=ParseMode.HTML)