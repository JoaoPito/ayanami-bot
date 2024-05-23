from langchain.agents import tool
from openai import OpenAI
from datetime import datetime
import vlc as v

VOICE = "nova"
MODEL = "tts-1"

FILE_PATH = f"downloaded/voice/{datetime.now().strftime('%s')}.mp3"

@tool
def voice(query: str) -> int:
    """Use this to speak out loud with the user. 
    The input to this toolco should be a comma separated list,
    the first part is the language you are speaking in the format 'lang:country' like in 'en:us', 
    the second part is a phrase or text you want to speak.
    Never use any markup language like Markdown"""
    args = query.split(',', 1)
    
    lang = args[0]
    text = args[1]

    try:

        client = OpenAI()
        with client.audio.speech.with_streaming_response.create(
            model="tts-1",
            voice="nova",
            input=text,
        ) as response:
            response.stream_to_file(FILE_PATH)

        mp3 = v.MediaPlayer(FILE_PATH)
        mp3.play()
    except Exception:
        return "Failed speaking out loud"
    else:
        return "Done!"

def create():
    return voice