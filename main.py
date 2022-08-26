from app import App
from sl_io import read, classify
from sl_func import translate, tts, arc_rect
from sl_graphics import round_polygon

from locale import currency
from tkinter import *
import os
import re
import json
import time
import math



class ui:
    root = Tk()
    last_time = int(round(time.time() * 1000))


    # CONST_DARK_COLOR = "#333333"
    # CONST_HIGHLIGHT_COLOR = "#FFFF82"
    # CONST_LIGHT_COLOR = "#F5F7DC"

    CONST_DARK_COLOR = "#f8acff"
    CONST_HIGHLIGHT_COLOR = "#f8acff"
    CONST_LIGHT_COLOR = "#696eff"
    CONST_HARDCODE_DARK_COLOR = "#333"

    def main(self):
        while (True):
            current_time = int(round(time.time() * 1000))
            if (current_time - self.last_time >= 500):
                #print("big update")
                self.root.update()
                self.last_time = current_time

            self.root.update_idletasks()

            code = self.app.decision()
            if (code == "W"): # write current character to text
                self.update_text()

            elif (code == "D"): # update current character
                self.char_c['text'] = self.app.char

            # elif (code == "S"): # speak in seperate audio thread

            elif (code == "C"): # clear text buffers
                self.update_text()

            elif (code == "B"): # backspace (delete last char in text)
                self.update_text()

    def update_text(self):
        self.text_eng.configure(text = self.app.text)
        self.text_other.configure(text = self.app.other_text)

    def __init__(self, ignore_fingers_path, bind_map_path, lang_to_code_path):

        self.app = App(ignore_fingers_path, bind_map_path, lang_to_code_path)

        self.root.update_idletasks()
        self.root.attributes('-fullscreen', True)

        dimensions = self.get_dimensions()
        # get diagonal dimensions (pythagorean :O)
        dimensions.append(int(math.sqrt(dimensions[0]**2 + dimensions[1]**2)))

        # dimensions = {}
        # dimensions[0] = 800 #width
        # dimensions[1] = 500 #height
        print(dimensions)


        self.canvas = Frame(self.root, width=dimensions[0], height=dimensions[1], bg=self.CONST_LIGHT_COLOR)
        # canvas = Canvas(self.root, width=800, height=500, bg=self.CONST_LIGHT_COLOR)
        self.canvas.grid(columnspan=4, rowspan=5)

        self.heading = Label(self.root, text="Sling", font=("Avenir", int(dimensions[1] / 16)), bg=self.CONST_LIGHT_COLOR, fg=self.CONST_DARK_COLOR)
        self.heading.grid(column=0, row=0, sticky="SW", padx=dimensions[0]/16)

        #TODO REMOVE TEST
        self.left_canvas = Canvas(self.root, width=dimensions[0]/2, height=dimensions[1] * 3/4, bg=self.CONST_LIGHT_COLOR)
        self.left_box = round_polygon(self.left_canvas, dimensions[0]/16, dimensions[1]/32, dimensions[0] * 7.5/16, dimensions[1] * 11/16, 20, width = 10, outline = "#FF0000", fill = "#00FF00")

        self.left_canvas.grid(column = 0, columnspan = 2, row = 1, rowspan = 2, sticky = "E")

        self.right_canvas = Canvas(self.root, width=dimensions[0]/2, height=dimensions[1] * 3/4, bg=self.CONST_LIGHT_COLOR)
        self.right_box = round_polygon(self.right_canvas, dimensions[0]/32, dimensions[1]/32, dimensions[0] * 7/16, dimensions[1] * 11/16, 20, width = 10, outline = "#FF0000", fill = "#00FF00")

        self.right_canvas.grid(column = 2, columnspan = 2, row = 1, rowspan = 2, sticky = "W")
        
        
        # ENGLISH SECTION ----------------------------------->

        self.expand_frame = Frame(self.root, height=dimensions[1]/2, bg=self.CONST_LIGHT_COLOR)
        self.expand_frame.grid(column=0, columnspan=2, row=2, sticky=N)

        self.h_eng = Label(self.root, text="Text (English)", font=("Avenir", int(dimensions[1]/32)), bg=self.CONST_HARDCODE_DARK_COLOR, fg=self.CONST_HIGHLIGHT_COLOR)
        self.h_eng.grid(column=0, row=1, sticky=NW, padx=dimensions[0] * 3/32, pady = (dimensions[1] * 3/32, 0))

        self.text_eng = Message(self.root, text="the pressure is getting wesser the pressure is getting wesser the pressure is getting wesser the pressure is getting wesser the pressure is getting wesser the pressure is getting wesser the pressure is getting wesser", font=("Avenir", int(dimensions[1]/40)), bg="white", fg=self.CONST_DARK_COLOR, width= dimensions[0] * 42/128)
        self.text_eng.grid(column=0, columnspan=2, row=2, sticky=NW, padx = (dimensions[0] * 3/32, 0))


        # OTHER LANGUAGES SECTION  --------------------------->
        # self.frameOther = Label(self.root, image=self.frameBox, bg=self.CONST_LIGHT_COLOR)
        # self.frameOther.grid(rowspan=2, columnspan=2, column=2, row=1, sticky=NS, ipady=20)

        options = self.app.lang_to_code.keys()

        # Text selected in dropdown
        self.clicked = StringVar(value="Select:")

        self.drop = OptionMenu(self.root, self.clicked, *options, command=self.app.change_language)
        self.drop.config(font=("Avenir", int(dimensions[1]/32)), fg=self.CONST_DARK_COLOR, bg=self.CONST_HARDCODE_DARK_COLOR, bd=0, height = int(dimensions[1]/640), width=15)
        self.drop.grid(column=2, row=1, sticky=NW, padx=(dimensions[0] * 1/16,0), pady = (dimensions[1] * 3/32, 0))

        self.text_other = Message(self.root, text="the pressure is getting wesser the pressure is getting wesser the pressure is getting wesser the pressure is getting wesser the pressure is getting wesser the pressure is getting wesser the pressure is getting wesser", font=("Avenir", int(dimensions[1]/40)), bg="white", fg=self.CONST_DARK_COLOR, width = dimensions[0] * 10/32)
        self.text_other.grid(column=2, columnspan=2, row=2, sticky=NW, padx = dimensions[0] * 1/16)


        # Current char --------------------------->
        self.cur_char_txt = Label(self.root, text="Current Character", font=("Avenir", 16), bg=self.CONST_LIGHT_COLOR, fg=self.CONST_DARK_COLOR)
        self.cur_char_txt.grid(column=0, row=3, sticky=E, padx=10)

        self.char_c = Message(self.root, text="a", font=("Avenir", 18), bg="white", fg=self.CONST_DARK_COLOR)
        self.char_c.grid(column=1, row=3, sticky=W)

        # Bottom btns ---------------------------->

        self.speak_icon = PhotoImage(file='img/volume-high.png')
        self.speak_icon = self.speak_icon.subsample(2,2)
        # img_label= Label(image=speak_icon)
        self.speak_btn= Button(self.root, image=self.speak_icon, borderwidth=0, bg=self.CONST_LIGHT_COLOR, command = lambda: tts(self.app.text,self.app.lang))
        self.speak_btn.grid(column=2, row=3, sticky=W, padx=40)

        self.speak_text = Label(self.root, text="Speak", font=("Avenir", 16), bg=self.CONST_LIGHT_COLOR, fg=self.CONST_DARK_COLOR)
        self.speak_text.grid(column=2, row=4, sticky=NW, padx=40)


        self.clear_icon = PhotoImage(file = 'img/close-circle.png')
        self.clear_icon = self.clear_icon.subsample(2,2)
        self.clear_btn = Button(self.root, image=self.clear_icon, borderwidth=0, bg=self.CONST_LIGHT_COLOR, command = lambda: self.app.clear)
        self.clear_btn.grid(column=3, row=3)

        self.clear_text = Label(self.root, text="Clear", font=("Avenir", 16), bg=self.CONST_LIGHT_COLOR, fg=self.CONST_DARK_COLOR)
        self.clear_text.grid(column=3, row=4, sticky=N)

        
    def get_dimensions(self):
        geometry = self.root.winfo_geometry()
        dimensions = str(geometry).replace("+", "x").split("x")
        int_dim = []
        for i in range(len(dimensions)):
            int_dim.append(int(dimensions[i]))
        return int_dim


bobby = ui("ignore_fingers.json", "binds.json", "lang.json")

bobby.main()

