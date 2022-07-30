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

current_char = " "
current_text = ""
current_lang = "en"

bind_map={}

def init_bindings(bmap):
    with open('binds.json', 'r') as f:
        bmap = json.load(f)
        print(bmap)


def read(ser):
    values = re.sub(r"[a-z'\\]", "", str(ser.readline())).split()
    print(values)
    return values

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
    return (bind_map.get(str(sum)))

def tts(read_text, read_lang):
    translator = Translator()
    new_text = str(translator.translate(read_text, read_lang, "en"))

    speak = gTTS(text=read_text, lang=read_lang)
    name = read_text.replace(" ", "_") + ".mp3"
    speak.save(name)
    os.system("mpg321 " + name)

def update(ser, bindings, text, lang):
    values = read(ser)
    print(values[0])
    if (str(values[0]) == "W"):
        current_text += current_char
    if (str(values[0]) == "D"):
        values.pop(0) #remove "D" from data
        print(values)
        current_char = classify(values, bindings)

    if (str(values[0]) == "S"):
        audio_thread = Thread(target=tts, args=[text, lang])
        audio_thread.start()

def main():
    init_bindings(bmap = bind_map)
    ser = serial.Serial('/dev/cu.SLAB_USBtoUART', baudrate = 115200, timeout=1)

    for i in range (100):
        #get rid of startup serial
        ser.readline()

    while True:
        update(ser=ser, bindings=bind_map, text = current_text, lang = current_lang)

if __name__ == "__main__":
    main()
