from app import App
from sl_io import read, classify
from sl_func import translate, tts, arc_rect


from locale import currency
from tkinter import *
import os
import re
import json



class ui:
    root = Tk()

    # CONST_DARK_COLOR = "#333333"
    # CONST_HIGHLIGHT_COLOR = "#FFFF82"
    # CONST_LIGHT_COLOR = "#F5F7DC"

    CONST_DARK_COLOR = "#f8acff"
    CONST_HIGHLIGHT_COLOR = "#f8acff"
    CONST_LIGHT_COLOR = "#696eff"
    CONST_HARDCODE_DARK_COLOR = "#333"

    #CONST_RANDOM_COLOR = "#333333"
    #CONST_MID_COLOR = "#828282"


    def __init__(self, ignore_fingers_path, bind_map_path, lang_to_code_path):
        # self.ignore_fingers = json.load(open(ignore_fingers_path))
        # self.bind_map = json.load(open(bind_map_path))
        # self.lang_to_code = json.load(open(lang_to_code_path))
        self.app = App(ignore_fingers_path, bind_map_path, lang_to_code_path)

        self.root.update_idletasks()
        self.root.attributes('-fullscreen', True)

        dimensions = self.get_dimensions()
        print(dimensions)


        canvas = Canvas(self.root, width=dimensions[0], height=dimensions[1], bg=self.CONST_LIGHT_COLOR)
        # canvas = Frame(self.root, width=800, height=500, bg=self.CONST_LIGHT_COLOR)
        canvas.grid(columnspan=4, rowspan=5)

#------------------------------------------------------------------------
        # points = round_rectangle(50, 50, 750, 500, radius=20, fill="blue")
        # rect = canvas.create_polygon(points, fill="blue", smooth=True)

        arc_rect(canvas, 100,100,600,400,100)

#------------------------------------------------------------------------


        heading = Label(self.root, text="Sling", font=("Avenir", 32), bg=self.CONST_LIGHT_COLOR, fg=self.CONST_DARK_COLOR)
        heading.grid(column=0, row=0, sticky=W, padx=35)
        
        # ENGLISH SECTION ----------------------------------->

        expand_frame = Frame(self.root, height=int(int(dimensions[1])/2), bg=self.CONST_LIGHT_COLOR)
        expand_frame.grid(column=0, columnspan=2, row=2, sticky=N)

        frameBox = PhotoImage(file='img/boxFrame.png')
        frameEng = Label(self.root, image=frameBox, bg=self.CONST_LIGHT_COLOR)
        frameEng.grid(rowspan=2, columnspan=2, column=0, row=1, sticky=NS, padx=17, ipady=20)

        h_eng = Label(self.root, text="Text (English)", font=("Avenir", 16), bg=self.CONST_HARDCODE_DARK_COLOR, fg=self.CONST_HIGHLIGHT_COLOR)
        h_eng.grid(column=0, row=1, sticky=NW, padx=35, pady=(30, 0))

        text_eng = Message(self.root, text="", font=("Avenir", 18), bg="white", fg=self.CONST_DARK_COLOR, width=320)
        text_eng.grid(column=0, columnspan=2, row=2, sticky=NW, padx=(30,0))


        # OTHER LANGUAGES SECTION  --------------------------->
        frameOther = Label(self.root, image=frameBox, bg=self.CONST_LIGHT_COLOR)
        frameOther.grid(rowspan=2, columnspan=2, column=2, row=1, sticky=NS, ipady=20)

        options = self.app.lang_to_code.keys()

        # Text selected in dropdown
        clicked = StringVar(value="Select:")

        drop = OptionMenu(self.root, clicked, *options, command=self.app.change_language)
        drop.config(font=("Avenir", 16), fg=self.CONST_DARK_COLOR, bg=self.CONST_HARDCODE_DARK_COLOR, bd=0, width=15)
        drop.grid(column=2, row=1, sticky=NW, padx=(35,0), pady=(30,0))

        text_other = Message(self.root, text="", font=("Avenir", 18), bg="white", fg=self.CONST_DARK_COLOR, width=int(float(dimensions[0]) * 0.4))
        text_other.grid(column=2, columnspan=2, row=2, sticky=NW, padx=(30,0))


        # Current char --------------------------->
        cur_char_txt = Label(self.root, text="Current Character", font=("Avenir", 16), bg=self.CONST_LIGHT_COLOR, fg=self.CONST_DARK_COLOR)
        cur_char_txt.grid(column=0, row=3, sticky=E, padx=10)

        char_c = Message(self.root, text="a", font=("Avenir", 18), bg="white", fg=self.CONST_DARK_COLOR)
        char_c.grid(column=1, row=3, sticky=W)

        # Bottom btns ---------------------------->

        speak_icon = PhotoImage(file='img/volume-high.png')
        speak_icon = speak_icon.subsample(2,2)
        # img_label= Label(image=speak_icon)
        speak_btn= Button(self.root, image=speak_icon, borderwidth=0, bg=self.CONST_LIGHT_COLOR, command = lambda: tts(self.app.text,self.app.lang))
        speak_btn.grid(column=2, row=3, sticky=W, padx=40)

        speak_text = Label(self.root, text="Speak", font=("Avenir", 16), bg=self.CONST_LIGHT_COLOR, fg=self.CONST_DARK_COLOR)
        speak_text.grid(column=2, row=4, sticky=NW, padx=40)


        clear_icon = PhotoImage(file = 'img/close-circle.png')
        clear_icon = clear_icon.subsample(2,2)
        clear_btn = Button(self.root, image=clear_icon, borderwidth=0, bg=self.CONST_LIGHT_COLOR, command = lambda: self.app.clear)
        clear_btn.grid(column=3, row=3)

        clear_text = Label(self.root, text="Clear", font=("Avenir", 16), bg=self.CONST_LIGHT_COLOR, fg=self.CONST_DARK_COLOR)
        clear_text.grid(column=3, row=4, sticky=N)

        """
        Workaround to get the size of the current screen in a multi-screen setup.

        Returns:
            geometry (str): The standard Tk geometry string.
                [width]x[height]+[left]+[top]
        """

        # self.root.attributes('-fullscreen', True)
        #self.root.state('iconic')

        self.root.mainloop()
        
    def get_dimensions(self):
        geometry = self.root.winfo_geometry()
        dimensions = str(geometry).replace("+", "x").split("x")
        return dimensions


bobby = ui("ignore_fingers.json", "binds.json", "lang.json")


