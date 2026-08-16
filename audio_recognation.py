import speech_recognition as sr
from db import Users

db = Users()



def voice_to_text(user_id, message):
    try:
        #log_info('Processing audio => text')
        recognizer = sr.Recognizer()

        with sr.AudioFile(f'audio/{user_id}_{message.message_id}.wav') as source:
            audio_data = recognizer.record(source)


            language = db.get_language(user_id)


            text = recognizer.recognize_google(audio_data, language=language)


        return text


    except Exception as e:
        #log_error(f'An error occurred in the audio_recognization file: {e}')
        return "Could not make out the speech."