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

def round_rectangle(x1, y1, x2, y2, radius=25, **kwargs):
        
    points = [x1+radius, y1,
              x1+radius, y1,
              x2-radius, y1,
              x2-radius, y1,
              x2, y1,
              x2, y1+radius,
              x2, y1+radius,
              x2, y2-radius,
              x2, y2-radius,
              x2, y2,
              x2-radius, y2,
              x2-radius, y2,
              x1+radius, y2,
              x1+radius, y2,
              x1, y2,
              x1, y2-radius,
              x1, y2-radius,
              x1, y1+radius,
              x1, y1+radius,
              x1, y1]

    return points

def arc_rect(canvas, x, y, w, h, c):
    canvas.create_arc(x,   y,   x+2*c,   y+2*c,   start= 90, extent=90, style="arc")
    canvas.create_arc(x+w-2*c, y+h-2*c, x+w, y+h, start=270, extent=90, style="arc")
    canvas.create_arc(x+w-2*c, y,   x+w, y+2*c,   start=  0, extent=90, style="arc")
    canvas.create_arc(x,   y+h-2*c, x+2*c,   y+h, start=180, extent=90, style="arc")
    canvas.create_line(x+c, y,   x+w-c, y    )
    canvas.create_line(x+c, y+h, x+w-c, y+h  )
    canvas.create_line(x,   y+c, x,     y+h-c)
    canvas.create_line(x+w, y+c, x+w,   y+h-c)