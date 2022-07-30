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

import json

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
        output[i] = re.sub(r"[a-z'\\]", "", str(values[i]))
    return output

def classify(values, bind_map):
    conc = {}
    for i in range(5):
        if (float(values[i])<=0.8):
            conc[i]=1
        else:
            conc[i]=0 #implied?

    sum = 0

    for i in range(5):
        sum += 2 ** i * conc[i]
    print(bind_map.get(str(sum)))
    print("sum: {0}".format(sum))

def main():

    bind_map={}

    with open('binds.json', 'r') as f:

        bind_map = json.load(f)
        print(bind_map)

    start = "These nuts! Hah, Goatee!"

    audio_thread = Thread(target=tts, args=[start, "en"])
    audio_thread.start()

    ser = serial.Serial('/dev/cu.SLAB_USBtoUART', baudrate = 115200, timeout=1)

    for i in range (100):
        #get rid of startup serial
        ser.readline()

    while True:
        #print(read(ser))
        print(classify(read(ser), bind_map))

    #ser.close()
    #audio_thread.join()

if __name__ == "__main__":
    main()







#from serial.tools import list_ports


#port = list(list_ports.comports())
#for p in port:
#    print(p.device)
