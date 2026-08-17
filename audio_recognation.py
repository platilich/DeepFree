import speech_recognition as sr
from db import Users

db = Users()



def voice_to_text(path_to_file):
    try:
        recognizer = sr.Recognizer()

        with sr.AudioFile(path_to_file) as source:
            audio_data = recognizer.record(source)


            text = recognizer.recognize_google(audio_data, language='ru-RU')


        return text


    except Exception as e:
        print(e)
        #log_error(f'An error occurred in the audio_recognization file: {e}')
        return "Could not make out the speech."