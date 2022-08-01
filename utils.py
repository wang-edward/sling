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
from helpers import bind_map, lang_to_code


class SlingStorage:
    def __init__(self, char, text, lang):
        self.char = char
        self.text = text
        self.lang = lang


curr = SlingStorage(".", "", "en")


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
    #print(ans)
    return (bind_map.get(str(sum)))


def translate(read_text, read_lang):
    translator = Translator()
    new_text = str(translator.translate(read_text, read_lang, "en"))
    return new_text


def tts(read_text, read_lang):
    translator = Translator()
    new_text = str(translator.translate(read_text, read_lang, "en"))

    speak = gTTS(text=new_text, lang=read_lang)
    name = read_text.replace(" ", "_") + ".mp3"
    speak.save(name)
    os.system("mpg321 " + name)


def update(ser, bindings, char, text, lang):
    values = read(ser)
    #print(values[0])
    if (str(values[0]) == "W"):
        if (curr.char != ""):
            curr.text += curr.char
    if (str(values[0]) == "D"):
        values.pop(0) #remove "D" from data
        #print(values)
        curr.char = classify(values, bindings)

    if (str(values[0]) == "S"):
        audio_thread = Thread(target=tts, args=[text, lang])
        audio_thread.start()


def change_language(selection):
    print(lang_to_code)
    curr.lang = lang_to_code.get(str(selection))
    print(curr.lang)


def main():
    translated_text = ""
    
    root = Tk()

    root.title('SLING DEMO')

    canvas = Frame(root, width=800, height=500, bg="#F5F7DC")
    canvas.grid(columnspan=4, rowspan=5)

    heading = Label(root, text="Sling", font=("Avenir", 32), bg="#F5F7DC", fg="#333333")
    heading.grid(column=0, row=0, sticky=W, padx=35)


    # ENGLISH SECTION ----------------------------------->
    h_eng = Label(root, text="English", font=("Avenir", 16), bg="#F5F7DC", fg="#333333", highlightthickness=2, highlightbackground="#FFFF82")
    h_eng.grid(column=0, row=1, sticky=SW, padx=35)

    frame_eng = Frame(root, width=250, height=200, bg="white")
    frame_eng.grid(columnspan=2, rowspan=1, column=0, row=2, ipadx=50, padx=35, sticky=W)

    text_eng = Message(root, text="applefe", font=("Avenir", 18), bg="white", fg="#333333", width=300)
    text_eng.grid(column=0, row=2, sticky=NW, padx=(40,0), pady=(25,0))


    # OTHER LANGUAGES SECTION  --------------------------->
    options = lang_to_code.keys()

    # Text selected in dropdown
    clicked = StringVar(value="Select:")

    drop = OptionMenu(root, clicked, *options, command=change_language)
    drop.config(font=("Avenir", 16), fg="#333333", bd=0, width=15)
    drop.grid(column=2, row=1, sticky=SW)
    drop["bg"]="#FFFF82"

    frame_other = Frame(root, width=250, height=200, bg="white")
    frame_other.grid(columnspan=2, rowspan=1, column=2, row=2, ipadx=50, sticky=W)

    text_other = Message(root, text="applefe", font=("Avenir", 18), bg="white", fg="#333333", width=300)
    text_other.grid(column=2, row=2, sticky=NW, pady=(25,0))


    # Current char --------------------------->
    cur_char_txt = Label(root, text="Current Character", font=("Avenir", 16), bg="#F5F7DC", fg="#333333")
    cur_char_txt.grid(column=0, row=3, sticky=E, padx=10)

    char_c = Message(root, text="a", font=("Avenir", 18), bg="white", fg="#333333")
    char_c.grid(column=1, row=3, sticky=W)

    # Bottom btns ---------------------------->

    speak_icon = PhotoImage(file='img/volume-high.png')
    #speak_icon = speak_icon.subsample(2,2)
    # img_label= Label(image=speak_icon)
    speak_btn= Button(root, image=speak_icon, borderwidth=0, bg="#F5F7DC")
    speak_btn.grid(column=2, row=3)

    speak_text = Label(root, text="Speak", font=("Avenir", 16), bg="#F5F7DC", fg="#333333")
    speak_text.grid(column=2, row=4, sticky=N)


    clear_icon = PhotoImage(file = 'img/close-circle.png')
    clear_btn = Button(root, image=clear_icon, borderwidth=0, bg="#F5F7DC")
    clear_btn.grid(column=3, row=3)

    clear_text = Label(root, text="Clear", font=("Avenir", 16), bg="#F5F7DC", fg="#333333")
    clear_text.grid(column=3, row=4, sticky=N)

    
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
        #print(len(values))
        if (len(values)==1 or len(values)==6):
            if (str(values[0]) == "W"):
                if (curr.char != None):
                    curr.text += curr.char
                    translated_text = translate(curr.text, curr.lang)
            elif (str(values[0]) == "D"):
                values.pop(0) #remove "D" from data
                #print(values)
                temp = classify(values, bind_map)
                #print(temp)
                curr.char = temp
                char_c['text'] = curr.char
                #curr.char = classify(values, bind_map)

            elif (str(values[0]) == "S"):
                audio_thread = Thread(target=tts, args=[curr.text, curr.lang])
                audio_thread.start()
            elif (str(values[0]) == "C"):
                curr.text = ""
            text_eng.configure(text=curr.text)
            text_other.configure(text=translated_text)
            #print("curr.char: {0}, curr.text: {1}".format(curr.char, curr.text))

if __name__ == "__main__":
    main()
