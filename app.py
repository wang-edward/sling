from tkinter import *
from python_translator import Translator
import json

from func import tts
from func import util_init

global current_char
global current_text
global current_lang
current_char = ""
global bind_map

def update(ser, bindings, char, text, lang):
    values = func.read(ser)
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

lang_to_code = {}

lang_data = json.load(open('lang.json'))

for i in lang_data["text"]:
    lang_to_code[i["language"]] = i["code"]


root = Tk()

def speech():
    # set text to smt
    p['text'] = "HAHAHAHhfioewhaiofhxeiowacmjfioewhajoicfheiwoahcfioewhaiocfheiwoahcfjiehifewhaciofheiowahcuoifheiwoahxfioewhaciofhewicFHUEWAHFUOEWHAUOFBEWJAFBUOEWHAUFHESOUAIHFUOESHAFUOBEAIWUFBEIHABUARUWAH"


root.title('SLING DEMO')

canvas = Frame(root, width=800, height=500, bg="#B5D99C")
canvas.grid(columnspan=5, rowspan=7)


heading = Label(root, text="SLING", font=("Avenir", 32), bg="#B5D99C", fg="#333333")
heading.grid(columnspan=3, column=1, row=0)

h2 = Label(root, text="Translated characters:", font=("Avenir", 16), bg="#B5D99C", fg="#333333")
h2.grid(columnspan=3, column=1, row=2)

p = Message(root, text="blahhhsh", font=("Avenir", 18), bg="#F5F7DC", fg="#333333")
p.grid(columnspan=3, column=1, row=3)

prompt = Label(root, text="Select a language in the dropdown below:", font=("Avenir", 16), bg="#B5D99C", fg="#333333")
prompt.grid(columnspan=3, column=1, row=4)


speech_text = StringVar()
speech_btn = Button(root, textvariable=speech_text, command=lambda:speech(), font="Avenir", bg="#828282", fg="#FFFF82", height=2, width=10)
speech_text.set("Speech")
speech_btn.grid(column=3, row=5, sticky=W)

options = lang_to_code.keys()

# Text selected in dropdown
clicked = StringVar(value="Select:")

drop = OptionMenu(root, clicked, *options)
drop.config(font=("Avenir", 16), fg="#333333", bd=0, width=15)
drop.grid(column=1, row=5, sticky=E)
drop["bg"]="#FFFF82"

util_init()

while True:
    tk.update_idletasks()
    tk.update()

root.mainloop()
