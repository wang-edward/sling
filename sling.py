#from tkinter import *
from struct import *
import serial
import time

from python_translator import Translator
import pyttsx3
from gtts import gTTS

from threading import Thread

import os

def tts(read_text, read_lang):
    translator = Translator()
    new_text = str(translator.translate(read_text, read_lang, "en"))

    speak = gTTS(text=read_text, lang=read_lang)
    name = read_text.replace(" ", "_") + ".mp3"
    speak.save(name)
    os.system("mpg321 " + name)

def main():


    translator = Translator()

    start = "These nuts! Hah, Goatee!"

    tts(start, "en")
    #ser = serial.Serial('/dev/cu.SLAB_USBtoUART', baudrate = 115200, timeout=1)
    #ser = serial.Serial('COM1', baudrate = 115200, timeout=1)

    #while True:
        #print(ser.read(27))
            #print(ser.readline())

    #ser.close()

if __name__ == "__main__":
    main()







#from serial.tools import list_ports


#port = list(list_ports.comports())
#for p in port:
#    print(p.device)
