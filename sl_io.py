import re
import serial
import time
import os
def read(ser):
    try:
        s = ser.readline()
        values = re.sub(r"[a-z'\\]", "", str(s)).split()
        # print(values)
        return values
    except:
        print("READ ERROR")
        return ""


def classify(values, bind_map, ignore_fingers):
    try:
        if (len(values)==5):
            conc = {}

            print("before: {0}".format(values))
            if (ignore_fingers != None):
                for x in ignore_fingers:
                    if (x==1):
                        values.pop(x)
            
            print("after: {0}".format(values))

            for i in range(len(values)):
                if (float(values[i])<=0.9):
                    conc[i]=1
                else:
                    conc[i]=0 #implied?
            sum = 0

            for i in range(len(values)):
                sum += 2 ** i * conc[i]
            print ("sum: {0}".format(sum))
            ans = bind_map.get(str(sum))
            return (bind_map.get(str(sum)))
    except:
        print("invalid INPUT")
        return "-1"

def write_buffer(text):
    cur = time.localtime()
    filename = "logs/" + str(cur.tm_year) + "." + str(cur.tm_mon) + "." + str(cur.tm_mday) + "." + str(cur.tm_hour) + "." + str(cur.tm_min) + "." + str(cur.tm_sec) + ".txt"
    f = open(filename, "w")
    f.write(text)

if __name__ == "__main__":
    print()
