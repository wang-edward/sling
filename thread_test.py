from tkinter import *
from struct import *
import serial
import time
from python_translator import Translator
from gtts import gTTS
from threading import Thread, active_count
import threading

import os
import struct
import re
from helpers import bind_map, lang_to_code

class App:

    #ser = serial.Serial('/dev/cu.SLAB_USBtoUART', baudrate = 115200, timeout=1)

    reading = False

    id = 1

    def read(self):
        print("read called")
        if (self.reading):
            print("reading is true")
            return
        #self.reading = True


        while (True):
            if (threading.active_count() <=3):
                print("number of threads: {0} current id: {1}".format(threading.active_count(), self))
                self.id+=1
                input_thread = Thread(target=self.read_wrapper,name='input_thread', daemon = True)
                input_thread.start()

        #self.reading = False

    def read_wrapper(self):
        time.sleep(1)

        #print(time.localtime())
        #s = self.ser.readline()
        #values = re.sub(r"[a-z'\\]", "", str(s)).split()
        #print(values)
        #return values

def main():
    sling = App()
    sling.read()
    while(True):
        x = input("give me somethign")

print(":ASDASDASD")


if __name__ == "__main__":
    print(":ASDASD")
    main()
    print("ASDASD`")
