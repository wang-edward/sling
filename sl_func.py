from python_translator import Translator
from gtts import gTTS
from threading import Thread
import os

def translate(read_text, read_lang, translator):
    try:
        new_text = str(translator.translate(read_text, read_lang, "english"))
        return new_text
    except:
        print("TRANSLATE FAILED")


def tts(read_text, read_lang, translator):
    print("read_text called")
    try:
        if (read_text.replace(" ","") != ""):
            print("this is read_text ({0})".format(read_text))
            new_text = str(translator.translate(read_text, read_lang, "english"))

            speak = gTTS(text=new_text, lang=lang_to_code[read_lang.title()])
            name = read_text.replace(" ", "_") + ".mp3"
            speak.save(name)
            os.system("mpg321 " + name)
    except:
        print("TTS FAILED")