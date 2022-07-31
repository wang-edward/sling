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

global current_char
global current_text
global current_lang



global bind_map

def read(ser):
    values = re.sub(r"[a-z'\\]", "", str(ser.readline())).split()
    #print(values)
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
    ans = bind_map.get(str(sum))
    print(ans)
    return (bind_map.get(str(sum)))

def tts(read_text, read_lang):
    translator = Translator()
    new_text = str(translator.translate(read_text, read_lang, "en"))

    speak = gTTS(text=read_text, lang=read_lang)
    name = read_text.replace(" ", "_") + ".mp3"
    speak.save(name)
    os.system("mpg321 " + name)

def update(ser, bindings, char, text, lang):
    values = read(ser)
    #print(values[0])
    if (str(values[0]) == "W"):
        if (current_char != ""):
            current_text += current_char
    if (str(values[0]) == "D"):
        values.pop(0) #remove "D" from data
        #print(values)
        current_char = classify(values, bindings)

    if (str(values[0]) == "S"):
        audio_thread = Thread(target=tts, args=[text, lang])
        audio_thread.start()

def main():
    current_char = "."
    current_text = ""
    current_lang = "en"
    with open('binds.json', 'r') as f:
        bind_map = json.load(f)
    print(bind_map)
    ser = serial.Serial('/dev/cu.SLAB_USBtoUART', baudrate = 115200, timeout=1)

    for i in range (100):
        #get rid of startup serial
        ser.readline()

    while True:
        values = read(ser)
        #print(values[0])
        if (str(values[0]) == "W"):
            if (current_char != None):
                current_text += current_char
        if (str(values[0]) == "D"):
            values.pop(0) #remove "D" from data
            #print(values)
            temp = classify(values, bind_map)
            print(temp)
            current_char = temp
            #current_char = classify(values, bind_map)

        if (str(values[0]) == "S"):
            audio_thread = Thread(target=tts, args=[current_text, current_lang])
            audio_thread.start()
        print("current_char: {0}, current_text: {1}".format(current_char, current_text))

if __name__ == "__main__":
    main()
