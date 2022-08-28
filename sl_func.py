from python_translator import Translator
from gtts import gTTS
from threading import Thread
import os

from tensorflow import keras
import pandas
import json

from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils
from sklearn.datasets import make_blobs
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline

def translate(read_text, read_lang, translator):
    try:
        new_text = str(translator.translate(read_text, read_lang, "english"))
        return new_text
    except:
        print("TRANSLATE FAILED")
        return "ERROR: Translate failed, check internet connection please :("


def tts(read_text, read_lang, translator, lang_to_code):
    print("TTS called")
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

def predict(model, values, alphabet_map):
    arr_2d = [values]
    ans_arr = model.predict(arr_2d)
    max_float = -1e9
    max_index = -1

    # make sure ans_arr is n x 1
    if len(ans_arr) > 1:
        return

    for i in range(len(ans_arr[0])):
        if ans_arr[0][i] > max_float:
            max_float = ans_arr[0][i]
            max_index = i

    return alphabet_map[str(max_index)]

def arc_rect(canvas, x, y, w, h, c):
    canvas.create_arc(x,   y,   x+2*c,   y+2*c,   start= 90, extent=90, style="arc")
    canvas.create_arc(x+w-2*c, y+h-2*c, x+w, y+h, start=270, extent=90, style="arc")
    canvas.create_arc(x+w-2*c, y,   x+w, y+2*c,   start=  0, extent=90, style="arc")
    canvas.create_arc(x,   y+h-2*c, x+2*c,   y+h, start=180, extent=90, style="arc")
    canvas.create_line(x+c, y,   x+w-c, y    )
    canvas.create_line(x+c, y+h, x+w-c, y+h  )
    canvas.create_line(x,   y+c, x,     y+h-c)
    canvas.create_line(x+w, y+c, x+w,   y+h-c)


if __name__ == "__main__":
    print("""
    =======================================================
        TEST MODEL PREDICTIONS
    =======================================================
    """)
    model = keras.models.load_model('.')
    values = [1.0,1.0,1.0,1.0,1.0]
    alphabet_dict = {}
    with open("alphabet.json", "r") as read_file:
        alphabet_dict = json.load(read_file)
        print(alphabet_dict)
        print(predict(model, values, alphabet_dict))
