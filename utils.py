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
from helpers import bind_map, lang_to_code


class SlingStorage:
    def __init__(self, char, text, other_text, lang, old_text):
        self.char = char
        self.text = text
        self.other_text = other_text
        self.lang = lang
        self.old_text = old_text


curr = SlingStorage(char="",text="",other_text="",lang="english", old_text="")


def read(ser):
    s = ser.readline()
    values = re.sub(r"[a-z'\\]", "", str(s)).split()
    print(values)
    return values


def classify(values, bind_map):
    print(len(values))
    if (len(values)==5):
        print("insdie")
        conc = {}
        for i in range(5):
            if (float(values[i])<=0.9):
                conc[i]=1
            else:
                conc[i]=0 #implied?
        sum = 0

        for i in range(5):
            sum += 2 ** i * conc[i]
        ans = bind_map.get(str(sum))
        #print(ans)
        return (bind_map.get(str(sum)))
    return ""


def translate(read_text, read_lang):
    translator = Translator()
    new_text = str(translator.translate(read_text, read_lang, "english"))
    return new_text


def tts(read_text, read_lang):
    print("read_text called")
    if (read_text.replace(" ","") != ""):
        print("this is read_text ({0})".format(read_text))
        print("ASDASDASD\n\n\n\n")
        translator = Translator()
        new_text = str(translator.translate(read_text, read_lang, "english"))

        speak = gTTS(text=new_text, lang=lang_to_code[read_lang.title()])
        name = read_text.replace(" ", "_") + ".mp3"
        speak.save(name)
        os.system("mpg321 " + name)

def change_language(selection):
    print(lang_to_code)
    #curr.lang = lang_to_code.get(str(selection))
    curr.other_text = translate(curr.text,curr.lang)
    curr.lang = str(selection.lower())
    print(curr.lang)

def clear():
    print("clear_called")
    curr.text = ""
    curr.other_text = "" # TODO Overwrite?


def main():
    root = Tk()

    root.title('SLING DEMO')

    canvas = Frame(root, width=800, height=500, bg="#F5F7DC")
    canvas.grid(columnspan=4, rowspan=5)

    heading = Label(root, text="Sling", font=("Avenir", 32), bg="#F5F7DC", fg="#333333")
    heading.grid(column=0, row=0, sticky=W, padx=35)


    # ENGLISH SECTION ----------------------------------->

    expand_frame = Frame(root, height=240, bg="#F5F7DC")
    expand_frame.grid(column=0, columnspan=2, row=2, sticky=N)

    frameBox = PhotoImage(file='img/boxFrame.png')
    frameEng = Label(root, image=frameBox, bg="#F5F7DC")
    frameEng.grid(rowspan=2, columnspan=2, column=0, row=1, sticky=NS, padx=17, ipady=20)

    h_eng = Label(root, text="Text (English)", font=("Avenir", 16), bg="#333333", fg="#FFFF82")
    h_eng.grid(column=0, row=1, sticky=NW, padx=35, pady=(30, 0))

    text_eng = Message(root, text="apple", font=("Avenir", 18), bg="white", fg="#333333", width=320)
    text_eng.grid(column=0, columnspan=2, row=2, sticky=NW, padx=(30,0))


    # OTHER LANGUAGES SECTION  --------------------------->
    frameOther = Label(root, image=frameBox, bg="#F5F7DC")
    frameOther.grid(rowspan=2, columnspan=2, column=2, row=1, sticky=NS, ipady=20)

    options = lang_to_code.keys()

    # Text selected in dropdown
    clicked = StringVar(value="Select:")

    drop = OptionMenu(root, clicked, *options, command=change_language)
    drop.config(font=("Avenir", 16), fg="#333333", bg='#333333', bd=0, width=15)
    drop.grid(column=2, row=1, sticky=NW, padx=(35,0), pady=(30,0))

    text_other = Message(root, text="applefe", font=("Avenir", 18), bg="white", fg="#333333", width=320)
    text_other.grid(column=2, columnspan=2, row=2, sticky=NW, padx=(30,0))


    # Current char --------------------------->
    cur_char_txt = Label(root, text="Current Character", font=("Avenir", 16), bg="#F5F7DC", fg="#333333")
    cur_char_txt.grid(column=0, row=3, sticky=E, padx=10)

    char_c = Message(root, text="a", font=("Avenir", 18), bg="white", fg="#333333")
    char_c.grid(column=1, row=3, sticky=W)

    # Bottom btns ---------------------------->

    speak_icon = PhotoImage(file='img/volume-high.png')
    speak_icon = speak_icon.subsample(2,2)
    # img_label= Label(image=speak_icon)
    speak_btn= Button(root, image=speak_icon, borderwidth=0, bg="#F5F7DC", command = tts)
    speak_btn.grid(column=2, row=3, sticky=W, padx=40)

    speak_text = Label(root, text="Speak", font=("Avenir", 16), bg="#F5F7DC", fg="#333333")
    speak_text.grid(column=2, row=4, sticky=NW, padx=40)


    clear_icon = PhotoImage(file = 'img/close-circle.png')
    clear_icon = clear_icon.subsample(2,2)
    clear_btn = Button(root, image=clear_icon, borderwidth=0, bg="#F5F7DC", command = clear)
    clear_btn.grid(column=3, row=3)

    clear_text = Label(root, text="Clear", font=("Avenir", 16), bg="#F5F7DC", fg="#333333")
    clear_text.grid(column=3, row=4, sticky=N)

    print(bind_map)
    ser = serial.Serial('/dev/cu.SLAB_USBtoUART', baudrate = 115200, timeout=1)

    for i in range (100):
        #get rid of startup serial
        print(i)
        ser.readline()
    print("agane")

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
                    print(curr.text)
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
                curr.other_text = ""
            elif(str(values[0]) == "B"):
                curr.text = curr.text[:-1]

            text_eng.configure(text=curr.text)
            text_other.configure(text=curr.other_text)
            print("curr.char: {0}, curr.text: {1}".format(curr.char, curr.text))

if __name__ == "__main__":
    main()
