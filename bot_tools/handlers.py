from aiogram import Router, F
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
    voice = message.voice
    file_id = voice.file_id

    # 2. Запрашиваем информацию о файле у Telegram
    file_info = await message.bot.get_file(file_id)
    file_path = file_info.file_path

    # 3. Скачиваем и сохраняем файл (например, в папку "voices")
    destination = f"voices/{voice.file_unique_id}.ogg"

    convert_ogg_to_wav(destination, f'voice/{voice.file_unique_id}.wav')

    tx = voice_to_text(f'voice/{voice.file_unique_id}.wav')

    await message.bot.download_file(file_path, destination=destination)

