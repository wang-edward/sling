from sl_io import read, classify, write_buffer
from sl_func import translate, tts

import json
import time
import serial
from threading import Thread
from python_translator import Translator
from gtts import gTTS

class dummy_serial:
    def readline(self):
        print("abc", end="")

class App:
    CONST_SERIAL = True # TODO replace depedning if plugged in or not
    CONST_POLL_TIME = 500

    reading = False
    shift = False
    practice = False
    char = ""
    text = ""
    other_text = ""
    lang = "english"
    last_time = 0
    target_text = "The quick brown fox jumps over the lazy dog"
    target_index = 0

    translator = Translator()

    if (CONST_SERIAL):
        ser = serial.Serial('/dev/cu.SLAB_USBtoUART', baudrate = 115200, timeout=1)
    else:
        ser = dummy_serial()

    def debug (self):
        print("""
            char = {0}
            text = {1}
            other_text = {2}
            lang = {3}
            shift = {4}
        """.format(self.char, self.text, self.other_text, self.lang, self.shift))
    
    def init_serial(self):
        if (self.CONST_SERIAL):
            for i in range(100):
                self.ser.readline()

    def __init__(self, ignore_fingers_path, bind_map_path0, bind_map_path1, lang_to_code_path):
        self.ignore_fingers = json.load(open(ignore_fingers_path))
        self.bind_map = json.load(open(bind_map_path0))
        self.bind_map1 = json.load(open(bind_map_path1))
        self.lang_to_code = json.load(open(lang_to_code_path))

    def change_language(self, selection):
        self.lang = str(selection.lower())
        self.other_text = translate(self.text, self.lang)

    def clear(self):
        temp_text = self.text
        self.text = ""
        self.other_text = ""
        write_thread = Thread(target=write_buffer, args=[temp_text])
        write_thread.start()

    def decision(self):
        values = []
        if (self.CONST_SERIAL):
            values = read(self.ser)
        if (len(values)!=1 and len(values)!=6):
            print("bad data or false")
            return
        
        code = str(values[0])
        print(values)
        self.debug()
        
        if (code == "W"): # write current character to text
            if (self.char == None):
                return
            if self.practice:
                if self.char == self.target_text[self.target_index]:
                    self.text += self.char
                    self.target_index += 1
                else:
                    return "D" # if char is not target char, ui should still reflect what is being inputted in 'current character' section
            else:
                self.text += self.char
                self.other_text = translate(self.text, self.lang, self.translator)
            return "W"
        elif (code == "D"): # update current character
            values.pop(0) # remove 'D'
            temp = ""
            if (self.shift == True):
                temp = classify(values, self.bind_map1, self.ignore_fingers)
            elif (self.shift == False):
                temp = classify(values, self.bind_map, self.ignore_fingers)

            self.char = temp
            return "D"
        elif (code == "S"): # speak in seperate audio thread
            try:
                audio_thread = Thread(target = tts, args=[self.text, self.lang, self.translator, self.lang_to_code])
                audio_thread.start()
                return "S"
            except:
                return "s"
        elif (code == "C"): # clear text buffers
            write_buffer(self.text)
            self.text = ""
            self.other_text = ""
            return "C"
        elif (code == "B"): # backspace (delete last char in text)
            print("""B
            B
            B
            B
            B
            B
            B
            B
            B
            B
            B""")
            print("before: {0}".format(self.text))
            self.text = self.text[0:-1]
            print("after: {0}".format(self.text))
            return "B"
        elif (code == "+"):
            self.shift = True
        elif (code == "-"):
            self.shift = False