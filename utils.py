from tkinter import *
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
    ans = bind_map.get(str(sum))
    #print(ans)
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
    lang_to_code = {}
    lang_data = json.load(open('lang.json'))
    for i in lang_data["text"]:
        lang_to_code[i["language"]] = i["code"]

    root = Tk()
    root.title("sling")
    canvas = Frame(root, width=800, height=500, bg="#B5D99C")
    canvas.grid(columnspan=5, rowspan=7)
    heading = Label(root, text="SLING", font=("Avenir", 32), bg="#B5D99C", fg="#333333")
    heading.grid(columnspan=3, column=1, row=0)
    h2 = Label(root, text="Translated characters: ", font=("Avenir", 16), bg="#B5D99C", fg="#333333")
    h2.grid(columnspan=3, column=1, row=2)
    p = Message(root, text=current_text, font=("Avenir", 18), bg="#F5F7DC", fg="#333333")
    p.grid(columnspan=3, column=1, row=3)
    prompt = Label(root, text="Select a language in the dropdown below:", font=("Avenir", 16), bg="#B5D99C", fg="#333333")
    prompt.grid(columnspan=3, column=1, row=4)
    speech_text = StringVar()
    speech_btn = Button(root, textvariable=speech_text, command=lambda:tts(current_text, current_lang), font="Avenir", bg="#828282", fg="#FFFF82", height=2, width=10)
    speech_text.set("Speech")
    speech_btn.grid(column=3, row=5, sticky=W)
    options = lang_to_code.keys()
# Text selected in dropdown
    clicked = StringVar(value="Select:")
    drop = OptionMenu(root, clicked, *options)
    drop.config(font=("Avenir", 16), fg="#333333", bd=0, width=15)
    drop.grid(column=1, row=5, sticky=E)
    drop["bg"]="#FFFF82"

    with open('binds.json', 'r') as f:
        bind_map = json.load(f)
    print(bind_map)
    ser = serial.Serial('/dev/cu.SLAB_USBtoUART', baudrate = 115200, timeout=1)

    for i in range (100):
        #get rid of startup serial
        ser.readline()

    while True:
        root.update_idletasks()
        root.update()
        values = read(ser)
        #print(values[0])
        print(len(values))
        if (len(values)==1 or len(values)==6):
            if (str(values[0]) == "W"):
                if (current_char != None):
                    current_text += current_char
            elif (str(values[0]) == "D"):
                values.pop(0) #remove "D" from data
                #print(values)
                temp = classify(values, bind_map)
                print(temp)
                current_char = temp
                #current_char = classify(values, bind_map)

            elif (str(values[0]) == "S"):
                audio_thread = Thread(target=tts, args=[current_text, current_lang])
                audio_thread.start()
            elif (str(values[0]) == "C"):
                current_text = ""
            p['text'] = current_text
            print("current_char: {0}, current_text: {1}".format(current_char, current_text))

if __name__ == "__main__":
    main()
