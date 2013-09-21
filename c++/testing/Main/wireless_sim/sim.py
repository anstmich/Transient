import serial
from time import sleep
import sys

arg = sys.argv[1]

fp = open('endurance.dat', 'r')
ser = serial.Serial(arg, 115200)
counter = 0
total = 0

for line in fp:
	ser.write(line)
	counter += 1
	
	if(counter >= 100):
		total += counter
		counter = 0
		print ''.join(['Sent ', str(total), ' packets.'])

	sleep(0.025)

fp.close()
ser.close()

