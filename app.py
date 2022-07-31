from tkinter import *
from turtle import bgcolor
from python_translator import Translator
import json

"""
Colour codes
Dark grey: #333333
Light grey: #828282
Yellow: #FFFF82
Off white: #F5F7DC
Green: #B5D99C
"""


lang_to_code = {}

lang_data = json.load(open('lang.json'))

for i in lang_data["text"]:
    lang_to_code[i["language"]] = i["code"]


root = Tk()

def speech():
    # set text to smt
    p['text'] = "HAHAHAHhfioewhaiofhxeiowacmjfioewhajoicfheiwoahcfioewhaiocfheiwoahcfjiehifewhaciofheiowahcuoifheiwoahxfioewhaciofhewicFHUEWAHFUOEWHAUOFBEWJAFBUOEWHAUFHESOUAIHFUOESHAFUOBEAIWUFBEIHABUARUWAH"


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

text_eng = Message(root, text="applefe", font=("Avenir", 18), bg="white", fg="#333333", width=200)
text_eng.grid(column=0, row=2, sticky=NW, padx=40, pady=25)



# OTHER LANGUAGES SECTION  --------------------------->
options = lang_to_code.keys()

# Text selected in dropdown
clicked = StringVar(value="Select:")

drop = OptionMenu(root, clicked, *options)
drop.config(font=("Avenir", 16), fg="#333333", bd=0, width=15)
drop.grid(column=2, row=1, sticky=SW)
drop["bg"]="#FFFF82"

frame_other = Frame(root, width=250, height=200, bg="white")
frame_other.grid(columnspan=2, rowspan=1, column=2, row=2, ipadx=50, sticky=W)

text_other = Message(root, text="applefe", font=("Avenir", 18), bg="white", fg="#333333", width=200)
text_other.grid(column=2, row=2, sticky=NW, pady=25)


# Current char --------------------------->
cur_char_txt = Label(root, text="Current Character", font=("Avenir", 16), bg="#F5F7DC", fg="#333333")
cur_char_txt.grid(column=0, row=3, sticky=E, padx=10)

char_c = Message(root, text="a", font=("Avenir", 18), bg="white", fg="#333333")
char_c.grid(column=1, row=3, sticky=W)

# Bottom btns ---------------------------->

speak_icon = PhotoImage(file='img/speak.png', width=50, height=50)
# img_label= Label(image=speak_icon)
speak_btn= Button(root, image=speak_icon, borderwidth=0, bg="#F5F7DC")
speak_btn.grid(column=2, row=3)


speak_text = Label(root, text="Speak", font=("Avenir", 16), bg="#F5F7DC", fg="#333333")
speak_text.grid(column=2, row=4, sticky=N)

clear_text = Label(root, text="Clear", font=("Avenir", 16), bg="#F5F7DC", fg="#333333")
clear_text.grid(column=3, row=4, sticky=N)


speech_text = StringVar()
# speech_btn = Button(root, textvariable=speech_text, command=lambda:speech(), font="Avenir", bg="#828282", fg="#FFFF82", height=2, width=10)
# speech_text.set("Speech")
# speech_btn.grid(column=3, row=5, sticky=W)

root.mainloop()
