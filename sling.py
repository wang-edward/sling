#from tkinter import *
from struct import *
import serial
import time

from python_translator import Translator
import pyttsx3
from gtts import gTTS

from threading import Thread

import os
import struct
import re

def tts(read_text, read_lang):
    translator = Translator()
    new_text = str(translator.translate(read_text, read_lang, "en"))

    speak = gTTS(text=read_text, lang=read_lang)
    name = read_text.replace(" ", "_") + ".mp3"
    speak.save(name)
    os.system("mpg321 " + name)

def read(ser):
    #line = (ser.readline()).replace("\r\n", "")

    line = ser.readline()
    values = line.split()

    output = {}

    for i in range(5):
        output[i] = re.sub("[a-z']", "", str(values[i]))
    return output

def main():

    start = "These nuts! Hah, Goatee!"

    audio_thread = Thread(target=tts, args=[start, "en"])
    audio_thread.start()

    ser = serial.Serial('/dev/cu.SLAB_USBtoUART', baudrate = 115200, timeout=1)

    for i in range (100):
        #get rid of startup serial
        ser.readline()

    while True:
        #print(ser.readline())
        print(read(ser))
        

    #ser.close()
    #audio_thread.join()

if __name__ == "__main__":
    main()







#from serial.tools import list_ports


#port = list(list_ports.comports())
#for p in port:
#    print(p.device)
