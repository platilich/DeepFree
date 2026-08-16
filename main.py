from openai import OpenAI

from config import second_api_key, second_server, second_model
from db import Users
import sys, time


db = Users()

client = OpenAI(api_key=second_api_key, base_url=second_server)
db.init_db()
db.add_user('1')




def think_animation():
    frames = ["Думаю.  ", "Думаю.. ", "Думаю..."]

    for frame in frames:
        sys.stdout.write(f"\r{frame}")
        sys.stdout.flush()
        time.sleep(0.3)  # скорость анимации



while True:
    userInput = input("- ")

    if (userInput.strip() != ""):
        db.update_conversation('1', f'user: {userInput}')

        think_animation()

        conversation = db.get_messages_list('1')
        print(conversation)

        response = client.chat.completions.create(
            model=second_model,
            messages=conversation,
            reasoning_effort="none"

        )

        response = response.choices[0].message.content


        sys.stdout.write("\r" + " " * 20 + "\r")  # затираем анимацию

        db.update_conversation('1', f'assistant: {response.replace('\n', ' ')}')
        print(response)


    else:
        print("Плохой запрос")