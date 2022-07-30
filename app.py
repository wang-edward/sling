from tkinter import *
from python_translator import Translator

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

options = [
    "en",
    "de",
    "es",
    "fr",
    "zh-CN",
    "zh-TW",
    "ja",
    "ko",
    "ar",
    "iw",
    "hi",
    "ur"
]

# Text selected in dropdown
clicked = StringVar(value="Select:")

drop = OptionMenu(root, clicked, *options)
drop.config(font=("Avenir", 16), fg="#333333", bd=0, width=5)
drop.grid(column=1, row=5, sticky=E)
drop["bg"]="#FFFF82"


root.mainloop()
