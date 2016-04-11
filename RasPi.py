import RPi.GPIO as GPIO
import Adafruit_DHT as dht
import picamera
import time
import random 
import os

def getFileName():
	return datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S.h264")

def secure_off():
	camera = picamera.PiCamera()
	camera.close()
	return {'info': "Secure Off"}

def secure_on(prevState, currState):
	pin = 4
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	camera = picamera.PiCamera()
	time.sleep(0.1)
	prevState = currState
	currState = GPIO.input(pin)
	if currState != prevState:
		newState = "HIGH" if currState else "LOW"
		return {'info': "GPIO pin %s is %s" % (pin, newState)}
		if currState:
			fileName = getFileName()
			print ("Starting Recording...")
			camera.start_preview()
			camera.start_recording(fileName)
			time.sleep(10)
			return {'info': fileName}
		else:
			camera.stop_preview()
			time.sleep(1)
			camera.stop_recording()
			return {'info': "Stopped Recording"}
	else:
		return {'info': "No motions"}

def motionauto(previous, current):
	motion = 4
	relay = [20, 21, 26]

	GPIO.setmode(GPIO.BCM)
	GPIO.setup(motion, GPIO.IN, GPIO.PUD_DOWN)
	GPIO.setup(relay, GPIO.OUT)
	GPIO.output(relay, GPIO.HIGH)

	previous = current
	current = GPIO.input(motion)
	if current != previous:
		new = "HIGH"
		GPIO.output(relay, GPIO.LOW)
		return {'info' :"GPIO pin %s is %s" % (motion, new)}
		time.sleep(10)
		#os.system("sudo omxplayer ring.mp3 &")
	else:
		GPIO.output(relay, GPIO.HIGH)
		return {"info": "No motions"}

def climate():
	pin = 3
	hum,temp = dht.read_retry(dht.DHT22, pin)
	humidity = float(round(hum))
	temperature = float(round(temp))
	return {'hum': humidity, 'temp': temperature}
	time.sleep(1)

def relay_off(pin):
	GPIO.setmode(GPIO.BCM)

	GPIO.setup(int(pin), GPIO.OUT)

	try:
		GPIO.output(int(pin), GPIO.HIGH)
		print('off', int(pin))
		return True
	except:
		return False

def relay_on(pin):
	GPIO.setmode(GPIO.BCM)

	GPIO.setup(int(pin), GPIO.OUT)
	GPIO.output(int(pin), GPIO.HIGH)

	try:
		GPIO.output(int(pin), GPIO.LOW)
		print('on', int(pin))
		return True
	except:
		return False
