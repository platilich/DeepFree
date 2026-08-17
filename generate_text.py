from openai import OpenAI

from config import second_api_key, second_server, second_model
from db import Users


db = Users()

client = OpenAI(api_key=second_api_key, base_url=second_server)
db.init_db()





def generate_response_text(user_id, prompt):
    db.update_conversation(user_id, f'user: {prompt}') # add user prompt to history

    conversation = db.get_messages_list(user_id) # get all history

    response = client.chat.completions.create(
        model=second_model,
        messages=conversation,
        reasoning_effort="none"

    )

    response = response.choices[0].message.content


    db.update_conversation(user_id, f'assistant: {response.replace('\n', ' ')}') #update history


    return response