#from tkinter import *
from struct import *
import serial
import time

from python_translator import Translator
import pyttsx3
from gtts import gTTS

import os

def tts(read_text, read_lang):
    speak = gTTS(text=read_text, lang=read_lang)
    name = read_text + ".mp3"
    speak.save(read_text + ".mp3")
    os.system("mpg321 " + name)

def main():


    translator = Translator()

    start = "These nuts! Hah, Goatee!"

    result = str(translator.translate(start, "es", "en"))

    start_tts = gTTS(text=start, lang='en')
    result_tts = gTTS(text=result, lang='es')

    #tts(start, "en")

    start_tts.save("start_tts.mp3")
    result_tts.save("end_tts.mp3")

    os.system("mpg321 start_tts.mp3")
    print("\n\n\n\n\n\n\n TEST \n\n\n\n\n\n\n")
    os.system("mpg321 end_tts.mp3")


    #ser = serial.Serial('/dev/cu.SLAB_USBtoUART', baudrate = 115200, timeout=1)
    #ser = serial.Serial('COM1', baudrate = 115200, timeout=1)

    #while True:
        #print(ser.read(27))
            #print(ser.readline())

    #ser.close()

if __name__ == "__main__":
    main()







#from serial.tools import list_ports


#port = list(list_ports.comports())
#for p in port:
#    print(p.device)
