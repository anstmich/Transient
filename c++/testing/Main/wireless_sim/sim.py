import serial
from time import sleep

fp = open('endurance.dat', 'r')
ser = serial.Serial('/dev/pts/4', 115200)

for line in fp:
    ser.write(line)
    print(line)
    sleep(0.05)

fp.close()
ser.close()

