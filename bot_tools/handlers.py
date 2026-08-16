from aiogram import Router, F
from aiogram.types import Message


from db import Users
from generate_text import generate_response_text


db = Users()


db.init_db()

router = Router()



@router.message(F.text)
async def text_input(message: Message):
    user_id = message.from_user.id
    text = message.text

    db.add_user(user_id)


    response = generate_response_text(user_id, text)

    await message.answer(response)