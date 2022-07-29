import tkinter as tk
# import PyPDF2

root = tk.Tk()

def speech():
    # set text to smt
    p['text'] = "HAHAHAHAH"


canvas = tk.Canvas(root, width=800, height=500, bg="#B5D99C")
canvas.grid(columnspan=3, rowspan=7)

heading = tk.Label(root, text="SLING", font=("Avenir", 32), bg="#B5D99C", fg="#333333")
heading.grid(column=1, row=0)

h2 = tk.Label(root, text="Translated characters:", font=("Avenir", 16), bg="#B5D99C", fg="#333333")
h2.grid(column=1, row=2)

p = tk.Label(root, text="blahhhsh", font=("Avenir", 18), bg="#F5F7DC", fg="#333333")
p.grid(column=1, row=3)

speech_text = tk.StringVar()
speech_btn = tk.Button(root, textvariable=speech_text, command=lambda:speech(), font="Avenir", bg="#828282", fg="#FFFF82", height=2, width=10)
speech_text.set("Speech")
speech_btn.grid(column=1, row=5)

root.mainloop()
