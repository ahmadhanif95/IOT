import RPi.GPIO as GPIO
import time
from gpiozero import DistanceSensor
import threading
import pyrebase


firebaseConfig = { "apiKey": "AIzaSyDJTgbkvUgSl8RRtJAoS8pRsd0JBjXOF44",
  "authDomain": "temp-1c73a.firebaseapp.com",
  "projectId": "temp-1c73a",
  "databaseURL":"https://temp-1c73a-default-rtdb.firebaseio.com/",
  "storageBucket": "temp-1c73a.appspot.com",
  "messagingSenderId": "445555880861",
  "appId": "1:445555880861:web:fdf19f33a3eac408213574",
  "measurementId": "G-L5D2C4BHP2"}

firebase=pyrebase.initialize_app(firebaseConfig)
db = firebase.database()




GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(18,GPIO.OUT,initial=GPIO.LOW) #sensor 1 giving sginal pin
GPIO.setup(15,GPIO.IN) #sensor 1 fall pin

GPIO.setup(5,GPIO.OUT,initial=GPIO.LOW) #sensor 2 giving sginal pin
GPIO.setup(6,GPIO.IN) #sensor 2 fall pin

GPIO.setup(17,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(27,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(22,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(10,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(9,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(11,GPIO.OUT,initial=GPIO.LOW)

sensor1 = DistanceSensor(echo=24, trigger=23)
sensor2 = DistanceSensor(echo=16, trigger=26)


def rest():
	GPIO.output(17,GPIO.LOW)
	GPIO.output(11,GPIO.LOW)
	GPIO.output(27,GPIO.LOW)
	GPIO.output(9,GPIO.LOW)
	GPIO.output(22,GPIO.LOW)
	GPIO.output(10,GPIO.LOW)



def normal():
	rest()
	
	GPIO.output(17,GPIO.HIGH)
	GPIO.output(11,GPIO.HIGH)
	v=1
	data = {"number":v}
	db.child("ahmad").update(data)
	#print ("RED")
	time.sleep(10)
	
	rest()
	
	GPIO.output(17,GPIO.LOW)
	GPIO.output(11,GPIO.LOW)

	GPIO.output(27,GPIO.HIGH)
	GPIO.output(9,GPIO.HIGH)
	#print ("YELLOW")
	v=2
	data = {"number":v}
	db.child("ahmad").update(data)
	time.sleep(3)
	
	GPIO.output(27,GPIO.LOW)
	GPIO.output(9,GPIO.LOW)

	GPIO.output(22,GPIO.HIGH)
	GPIO.output(10,GPIO.HIGH)
	#print ("GREEN")
	
	v=3
	data = {"number":v}
	db.child("ahmad").update(data)
	time.sleep(10)
	rest()
	
	
	GPIO.output(22,GPIO.LOW)
	GPIO.output(10,GPIO.LOW)
	GPIO.output(27,GPIO.HIGH)
	GPIO.output(9,GPIO.HIGH)
	#print ("YELLOW")
	v=2
	data = {"number":v}
	db.child("ahmad").update(data)
	time.sleep(3)
	GPIO.output(27,GPIO.LOW)
	GPIO.output(9,GPIO.LOW)



def my_callback1(NUM1):
	rest()
	GPIO.output(17,GPIO.HIGH)
	GPIO.output(11,GPIO.HIGH)
	v=1
	data = {"number":v}
	db.child("ahmad").update(data)
	#GPIO.output(27,GPIO.HIGH)
	#GPIO.output(9,GPIO.HIGH)
	#print ("YELLOW")




def my_callback2(NUM2):
	rest()
	GPIO.output(10,GPIO.HIGH)
	GPIO.output(22,GPIO.HIGH)
	v=3
	data = {"number":v}
	db.child("ahmad").update(data)
	



def ultra1():
	while True:
		distance1= sensor1.distance * 100
		print('Distance1: ', distance1)
		if distance1<10:
			GPIO.output(18,GPIO.LOW)
		else:
			GPIO.output(18,GPIO.HIGH)
		time.sleep(0.5)
		print(GPIO.input(18))

def ultra2():
	while True:
		distance2= sensor2.distance * 100
		print('Distance2: ', distance2)
		if distance2<15:
			GPIO.output(5,GPIO.LOW)
		else:
			GPIO.output(5,GPIO.HIGH)
		time.sleep(0.5)
		print(GPIO.input(5))

def TURN1():
	while True:
		moaz=db.child("/ahmad/TURN1").get()
		if moaz.val()=="1":
			GPIO.output(18,GPIO.LOW)
			v=0
			data = {"TURN1":v}
			db.child("moaz").update(data)
		else:
			GPIO.output(18,GPIO.HIGH)
			
		
			

def TURN2():
	while True:
		moaz=db.child("/ahmad/TURN2").get()
		if moaz.val()=="1":
			GPIO.output(5,GPIO.LOW)
			v=0
			data = {"TURN2":v}
			db.child("moaz").update(data)
			
		else:
			GPIO.output(5,GPIO.HIGH)
			
			
			
			
thread1 = threading.Thread(target=ultra1)
thread1.start()			

thread2 = threading.Thread(target=ultra2)
thread2.start()


thread3 = threading.Thread(target=TURN1)
thread3.start()

thread4 = threading.Thread(target=TURN2)
thread4.start()


GPIO.add_event_detect(15, GPIO.FALLING, callback=my_callback1)
GPIO.add_event_detect(6, GPIO.FALLING, callback=my_callback2)



while True:
	normal()