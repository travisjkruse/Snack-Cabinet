import serial
import datetime
import time
import threading
import RPi.GPIO as GPIO

ser = serial.Serial('/dev/ttyACM0',9600,timeout=1)
time.sleep(1)

GPIO.setmode(GPIO.BOARD)

#Initialize LED GPIO pins
GPIO.setup(16,GPIO.OUT) #Green
GPIO.setup(24,GPIO.OUT) #Red
#Initialize lighting GPIO pins
GPIO.setup(19,GPIO.OUT)
GPIO.setup(11,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
GPIO.setup(15,GPIO.OUT)
#Initialize lock GPIO pins
GPIO.setup(21,GPIO.OUT)
GPIO.setup(23,GPIO.OUT)

#Initial output
GPIO.output(24,GPIO.HIGH) #Red LED ON
GPIO.output(16,GPIO.LOW) #Green LED OFF
GPIO.output(21,GPIO.HIGH) #Lock 1 ON
GPIO.output(23,GPIO.HIGH) #Lock 2 ON
GPIO.output(19,GPIO.LOW) #Light 1 OFF
GPIO.output(11,GPIO.LOW) #Light 2 OFF
GPIO.output(13,GPIO.LOW) #Light 3 OFF
GPIO.output(15,GPIO.LOW) #Light 4 OFF

now = datetime.datetime.now()
with open('/var/www/log.html', 'a') as f:
	f.write('\n<no>Cabinet Boot</no> at '+str(now)+'<br />')

class greenBlink(threading.Thread):
	def run(self):
		for i in range(3):
			print('Green blink')
			GPIO.output(16,GPIO.HIGH)
			time.sleep(0.25)
			GPIO.output(16,GPIO.LOW)
			time.sleep(0.25)
class redBlink(threading.Thread):
	def run(self):
		for i in range(3):
			print('Red blink')
			GPIO.output(24,GPIO.LOW)
			time.sleep(0.25)
			GPIO.output(24,GPIO.HIGH)
			time.sleep(0.25)
class openCase(threading.Thread):
	def run(self):
		print('Case Open')
		print('Lights on')
		GPIO.output(21,GPIO.LOW) #Lock 1 OFF
		GPIO.output(23,GPIO.LOW) #Lock 2 OFF
		GPIO.output(19,GPIO.HIGH) #Light 1 ON
		GPIO.output(11,GPIO.HIGH) #Light 2 ON
		GPIO.output(13,GPIO.HIGH) #Light 3 ON
		GPIO.output(15,GPIO.HIGH) #Light 4 ON
		time.sleep(5)
		print('Case Closed')
		GPIO.output(21,GPIO.HIGH) #Lock 1 ON
		GPIO.output(23,GPIO.HIGH) #Lock 2 ON
		time.sleep(60)
		print('Lights off')
		GPIO.output(19,GPIO.LOW) #Light 1 OFF
		GPIO.output(11,GPIO.LOW) #Light 2 OFF
		GPIO.output(13,GPIO.LOW) #Light 3 OFF
		GPIO.output(15,GPIO.LOW) #Light 4 OFF

while 1:
    line = ser.readline()
    if len(line) != 0 and int(line).bit_length() <= 18 and int(line).bit_length() >=17:
		blinkGreen = greenBlink()
		blinkRed = redBlink()
		caseOpen = openCase()     
		now = datetime.datetime.now()
		if line in open('/home/pi/SnackStats/Permissions.txt').read():
			print(''+line+'\t'+str(now)+'\tOK'+'\n')
			blinkGreen.start()
			caseOpen.start()
			with open('/var/www/log.html', 'a') as f:
			        f.write('\n<idnum>'+line+'</idnum>&emsp;'+str(now)+'&emsp;<ok>OK</ok><br />')
		else:
			print(''+line+'\t'+str(now)+'\tNO'+'\n')
			blinkRed.start()
			with open('/var/www/log.html', 'a') as f:
	        		f.write('\n<idnum>'+line+'</idnum>&emsp;'+str(now)+'&emsp;<no>NO</no><br />')


		            
