from pydub import AudioSegment



def convert_ogg_to_wav(input_file, output_file):
    try:
        #log_info('translating ogg => wav in the file_convertor file')
        # Load the OGG file
        audio = AudioSegment.from_ogg(input_file)

        # Export as MP3 with desired bitrate
        audio.export(output_file, format="wav")


    except Exception as e:
        print(e)
        #log_error(f'An error has occurred in the file_convertor file: {e}')