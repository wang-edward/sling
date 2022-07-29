#from tkinter import *
from struct import *
import serial
import time

from python_translator import Translator
import pyttsx3
from gtts import gTTS

import os



translator = Translator()

start = "These nuts! Hah, Goatee!"
result = str(translator.translate(start, "spanish", "english"))

start_tts = gTTS(text=start, lang='en')
result_tts = gTTS(text=result, lang='en')

start_tts.save("start_tts.mp3")
result_tts.save("end_tts.mp3")

os.system("mpg321 start_tts.mp3")
os.system("mpg321 end_tts.mp3")

print (result)

#engine = pyttsx3.init()
#engine.say(start)
#engine.say(result)
#engine.runAndWait();


#ser = serial.Serial('/dev/cu.SLAB_USBtoUART', baudrate = 115200, timeout=1)
#ser = serial.Serial('COM1', baudrate = 115200, timeout=1)

time.sleep(1)
#while True:
    #print(ser.read(27))
    #print(ser.readline())

#ser.close()









#from serial.tools import list_ports


#port = list(list_ports.comports())
#for p in port:
#    print(p.device)
