from sl_io import read, classify
from sl_func import translate, tts

import json
import time
import serial
from threading import Thread
from python_translator import Translator
from gtts import gTTS

class dummy_serial:
    def readline(self):
        print("abc")

class App:
    CONST_SERIAL = False # TODO replace depedning if plugged in or not
    CONST_POLL_TIME = 500

    reading = False
    char = ""
    text = ""
    other_text = ""
    lang = "english"
    old_text = ""
    last_time = 0

    translator = Translator()

    if (CONST_SERIAL):
        ser = serial.Serial('/dev/cu.SLAB_USBtoUART', baudrate = 115200, timeout=1)
    else:
        ser = dummy_serial()
    
    def init_serial(self):
        if (self.CONST_SERIAL):
            for i in range(100):
                self.ser.readline()

    def __init__(self, ignore_fingers_path, bind_map_path, lang_to_code_path):
        self.ignore_fingers = json.load(open(ignore_fingers_path))
        self.bind_map = json.load(open(bind_map_path))
        self.lang_to_code = json.load(open(lang_to_code_path))

    def change_language(self, selection):
        self.lang = str(selection.lower())
        self.other_text = translate(self.text, self.lang)

    def clear(self):
        temp_text = self.text
        self.text = ""
        self.other_text = ""
        write_thread = Thread(target=self.backup, args=[temp_text])
        write_thread.start()

    def backup(self, write_text):
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        f = open(t, "a")
        f.write(write_text)
        f.close()

    def decision(self):
        values = []
        if (self.CONST_SERIAL):
            values = read(self.ser)
        if (not len(values)==1 or len(values)==6):
            return
        
        code = str(values[0])
        print(code)
        
        if (code == "W"): # write current character to text
            if (self.char == None):
                return
            self.text += self.char
            self.other_text = translate(self.text, self.lang, self.translator)
            return "W"
        elif (code == "D"): # update current character
            values.pop[0]
            temp = classify(values, self.bind_map, self.ignore_fingers)
            self.char = temp
            print(self.char)
            return "D"
        elif (code == "S"): # speak in seperate audio thread
            try:
                audio_thread = Thread(target = tts, args=[self.text, self.lang, self.translator])
                audio_thread.start()
                return "S"
            except:
                return "s"
        elif (code == "C"): # clear text buffers
            self.text = ""
            self.other_text = ""
            return "C"
        elif (code == "B"): # backspace (delete last char in text)
            self.text = self.text[0:-1]
            return "B"

            
        

