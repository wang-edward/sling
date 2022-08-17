from sl_io import read, classify
from sl_func import translate, tts

import json
import time
import serial
from threading import Thread

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

    if (CONST_SERIAL):
        ser = serial.Serial('/dev/cu.SLAB_USBtoUART', baudrate = 115200, timeout=1)
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
        current_time = int(round(time.time() * 1000))
        if (current_time - self.last_time >= self.CONST_POLL_TIME):

