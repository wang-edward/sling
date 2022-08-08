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

    hand = PhotoImage(file = 'img/hand.png')

    label1 = Label(image = hand)
    label1.grid(rowspan=2, columnspan=2, column=2, row=1, sticky=NS, ipady=20)


    # Text selected in dropdown
    clicked = StringVar(value="Select:")

    drop = OptionMenu(root, clicked, *options)
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
    speak_btn= Button(root, image=speak_icon, borderwidth=0, bg="#F5F7DC")
    speak_btn.grid(column=2, row=3, sticky=W, padx=40)

    speak_text = Label(root, text="Speak", font=("Avenir", 16), bg="#F5F7DC", fg="#333333")
    speak_text.grid(column=2, row=4, sticky=NW, padx=40)


    clear_icon = PhotoImage(file = 'img/close-circle.png')
    clear_icon = clear_icon.subsample(2,2)
    clear_btn = Button(root, image=clear_icon, borderwidth=0, bg="#F5F7DC")
    clear_btn.grid(column=3, row=3)

    clear_text = Label(root, text="Clear", font=("Avenir", 16), bg="#F5F7DC", fg="#333333")
    clear_text.grid(column=3, row=4, sticky=N)

    while True:
        root.update_idletasks()
        root.update()

if __name__ == "__main__":
    main()
