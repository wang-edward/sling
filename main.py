from app import App
from sl_io import read, classify
from sl_func import translate, tts, arc_rect
from sl_graphics import round_polygon

from locale import currency
from tkinter import *
import tkinter.scrolledtext
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

    def update_text(self):

        # self.text_eng.configure(state = 'normal')
        self.text_eng.replace("1.0", tkinter.END, self.app.text)
        # self.text_eng.configure(state = 'disabled')

        # self.text_other.configure(state = 'normal')
        self.text_other.replace("1.0", tkinter.END, self.app.other_text)
        # self.text_other.configure(state = 'disabled')

    def main(self):
        while (True):
            current_time = int(round(time.time() * 1000))
            if (current_time - self.last_time >= 1000):
                self.root.update()
                self.last_time = current_time

            self.root.update_idletasks()

            code = self.app.decision()
            # print("code: {0}".format(code))
            if (code == "W"): # write current character to text
                self.update_text()

            elif (code == "D"): # update current character
                self.char_c['text'] = self.app.char

            # elif (code == "S"): # speak in seperate audio thread

            elif (code == "C"): # clear text buffers
                self.update_text()

            elif (code == "B"): # backspace (delete last char in text)
                self.update_text()

    def __init__(self, ignore_fingers_path, bind_map_path0, bind_map_path1, lang_to_code_path):

        self.app = App(ignore_fingers_path, bind_map_path0, bind_map_path1, lang_to_code_path)

        self.root.update_idletasks()
        self.root.attributes('-fullscreen', True)

        dimensions = self.get_dimensions()
        # get diagonal dimensions (pythagorean :O)
        dimensions.append(int(math.sqrt(dimensions[0]**2 + dimensions[1]**2)))

        # dimensions = {}
        # dimensions[0] = 800 #width
        # dimensions[1] = 500 #height
        print(dimensions)


        self.canvas = Frame(self.root, width=dimensions[0], height=dimensions[1], bg=self.CONST_LIGHT_COLOR, borderwidth=0, highlightthickness=0)
        # canvas = Canvas(self.root, width=800, height=500, bg=self.CONST_LIGHT_COLOR)
        self.canvas.grid(columnspan=4, rowspan=5)

        self.heading = Label(self.root, text="Sling", font=("Avenir", int(dimensions[1] / 16)), bg=self.CONST_LIGHT_COLOR, fg=self.CONST_DARK_COLOR, borderwidth=0, highlightthickness=0)
        self.heading.grid(column=0, row=0, sticky="SW", padx=(dimensions[0]/16, 0))

        self.border_thickness = 5

        #TODO REMOVE TEST
        self.left_canvas = Canvas(self.root, width=dimensions[0]/2, height=dimensions[1] * 3/4, bg=self.CONST_LIGHT_COLOR, highlightthickness=0)
        self.left_box = round_polygon(self.left_canvas, dimensions[0]/16, dimensions[1]/32, dimensions[0] * 7.5/16, 
        dimensions[1] * 11/16, 20, width = self.border_thickness, outline = self.CONST_HIGHLIGHT_COLOR, fill = self.CONST_HARDCODE_DARK_COLOR)
        self.left_canvas.create_line(dimensions[0] / 16, dimensions[1]/6.25, dimensions[0] * 7.5/16, dimensions[1]/6.25, fill=self.CONST_HIGHLIGHT_COLOR, width=self.border_thickness)



        self.left_canvas.grid(column = 0, columnspan = 2, row = 1, rowspan = 2, sticky = "E")

        self.right_canvas = Canvas(self.root, width=dimensions[0]/2, height=dimensions[1] * 3/4, bg=self.CONST_LIGHT_COLOR, highlightthickness=0)
        self.right_box = round_polygon(self.right_canvas, dimensions[0]/32, dimensions[1]/32, dimensions[0] * 7/16, dimensions[1] * 11/16, 20, width = self.border_thickness, outline = self.CONST_HIGHLIGHT_COLOR, fill = self.CONST_HARDCODE_DARK_COLOR)
        self.right_canvas.create_line(dimensions[0] / 32, dimensions[1]/6.25, dimensions[0] * 7/16, dimensions[1]/6.25, fill=self.CONST_HIGHLIGHT_COLOR, width=self.border_thickness)


        self.right_canvas.grid(column = 2, columnspan = 2, row = 1, rowspan = 2, sticky = "W")
        
        
        # ENGLISH SECTION ----------------------------------->

        self.h_eng = Label(self.root, text="Text (English)", font=("Avenir", int(dimensions[1]/32)), bg=self.CONST_HARDCODE_DARK_COLOR, fg=self.CONST_HIGHLIGHT_COLOR)
        self.h_eng.grid(column=0, row=1, sticky=NW, padx=dimensions[0] * 3/32, pady = (dimensions[1] * 3/32, 0))

        # self.text_eng = Message(self.root, text="the pressure is getting wesser the pressure is getting wesser the pressure is getting wesser the pressure is getting wesser the pressure is getting wesser the pressure is getting wesser the pressure is getting wesser", font=("Avenir", int(dimensions[1]/40)), bg="white", fg=self.CONST_DARK_COLOR, width= dimensions[0] * 43/128)

        self.text_eng = tkinter.scrolledtext.ScrolledText(self.root, width=int(dimensions[0] * 13/512), height=int(dimensions[1]/64), font=("Avenir", int(dimensions[1]/40)), wrap = tkinter.WORD)
        self.text_eng.grid(column=0, columnspan=2, row=2, sticky=NW, padx = (dimensions[0] * 3/32, 0))
        # self.text_eng.configure(state = 'disabled')


        # OTHER LANGUAGES SECTION  --------------------------->
        # self.frameOther = Label(self.root, image=self.frameBox, bg=self.CONST_LIGHT_COLOR)
        # self.frameOther.grid(rowspan=2, columnspan=2, column=2, row=1, sticky=NS, ipady=20)

        options = self.app.lang_to_code.keys()

        # Text selected in dropdown
        self.clicked = StringVar(value="Select:")

        self.drop = OptionMenu(self.root, self.clicked, *options, command=self.app.change_language)
        self.drop.config(font=("Avenir", int(dimensions[1]/32)), fg=self.CONST_DARK_COLOR, bg=self.CONST_HARDCODE_DARK_COLOR, bd=0, height = int(dimensions[1]/640), width=int(dimensions[0] / 100))
        self.drop.grid(column=2, row=1, sticky=NW, padx=(dimensions[0] * 1/16,0), pady = (dimensions[1] * 3/32, 0))

        self.text_other = tkinter.scrolledtext.ScrolledText(self.root, width=int(dimensions[0] * 13/512), height=int(dimensions[1]/64), font=("Avenir", int(dimensions[1]/40)), wrap = tkinter.WORD)
        self.text_other.grid(column=2, columnspan=2, row=2, sticky="nw", padx = dimensions[0] * 1/16)
        # self.text_other.configure(state = 'disabled')

        # Current char --------------------------->
        self.cur_char_txt = Label(self.root, text="Current Character: ", font=("Avenir", int(dimensions[1]/32)), bg=self.CONST_LIGHT_COLOR, fg=self.CONST_DARK_COLOR)
        self.cur_char_txt.grid(column=0, row=3, sticky=E)

        self.char_c = Message(self.root, text="_", font=("Avenir", int(dimensions[1]/32)), bg="white", fg=self.CONST_DARK_COLOR)
        self.char_c.grid(column=1, row=3, sticky=W)

        # Bottom btns ---------------------------->

        self.speak_icon = PhotoImage(file='img/volume-high.png')
        self.speak_icon = self.speak_icon.subsample(2,2)
        # img_label= Label(image=speak_icon)
        self.speak_btn= Button(self.root, image=self.speak_icon, borderwidth=0, bg=self.CONST_LIGHT_COLOR, command = lambda: tts(self.app.text,self.app.lang, self.app.translator, self.app.lang_to_code))
        self.speak_btn.grid(column=2, row=3, sticky=W, padx=40)

        self.speak_text = Label(self.root, text="Speak", font=("Avenir", int(dimensions[1]/40)), bg=self.CONST_LIGHT_COLOR, fg=self.CONST_DARK_COLOR)
        self.speak_text.grid(column=2, row=4, sticky=NW, padx=40)

        self.clear_icon = PhotoImage(file = 'img/close-circle.png')
        self.clear_icon = self.clear_icon.subsample(2,2)
        self.clear_btn = Button(self.root, image=self.clear_icon, borderwidth=0, bg=self.CONST_LIGHT_COLOR, command = lambda: self.app.clear)
        self.clear_btn.grid(column=3, row=3)

        self.clear_text = Label(self.root, text="Clear", font=("Avenir", int(dimensions[1]/40)), bg=self.CONST_LIGHT_COLOR, fg=self.CONST_DARK_COLOR)
        self.clear_text.grid(column=3, row=4, sticky=N)

        
    def get_dimensions(self):
        geometry = self.root.winfo_geometry()
        dimensions = str(geometry).replace("+", "x").split("x")
        int_dim = []
        for i in range(len(dimensions)):
            int_dim.append(int(dimensions[i]))
        return int_dim

if __name__ == "__main__":

    bobby = ui("ignore_fingers.json", "binds.json", "binds1.json", "lang.json")
    bobby.main()