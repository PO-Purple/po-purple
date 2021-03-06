from BrickPi import *
import threading
import time
import RPi.GPIO as GPIO
BrickPiSetup()

# Class concerning the LEGO-MINDSTORM Motor
# It possible to let the motor run (back and forth) at a given power rate.
# It's possible to rotate over a given angle. 
class Motor:
    def __init__(self,port):
        ## A motor is connected to a given port ('A','B','C','D')
        self.__port = port
        ## BrickPi command to enable the motor
        exec("BrickPi.MotorEnable[PORT_" + self.__port + "] = 1")
        ## Variable storring the actual moving status of this motor
        ## speed = 0 is not running
        ## speed < 0 is running backward
        ## speed > 0 is running forward
        self.__speed = 0
        self.__thread = None
	self.__count = 0
	
    ## Returning the running speed of this Motor
    ## speed = 0 is not running
    ## speed < 0 is running backward
    ## speed > 0 is running forward
    def get_speed(self):
        return self.__speed
    
    ## Let's run the motor
    def run_motor(self):
	result = BrickPiUpdateValues()
	if not result:
		exec('old_angle = BrickPi.Encoder[PORT_'+self.__port+']')
	else:
	    old_angle = 0
	while (self.__speed !=0):
	     result = BrickPiUpdateValues()
	     if not result:
		     exec('angle = BrickPi.Encoder[PORT_'+self.__port+']')
	     else:
		angle = 0  
	     self.update_count(old_angle,angle)
	     old_angle = angle
             exec("BrickPi.MotorSpeed[PORT_" + self.__port + "] =" + str(self.__speed))
             BrickPiUpdateValues()
    # update the value of self.__count
    # if angle < old_angle: value = (720-old_angle) + angle
    # else: value = angle - old_angle
    def update_count(self,old_angle,angle):
        value = (angle-old_angle)/720.
        self.__count = value
    # A method returning the number of rotations of the motor since the last time
    # reset_count() is executed
    def get_count(self):
	return self.__count
    # A method to reset the counter
    def reset_count(self):
	self.__count = 0
    # A method to turn the motor on
    def on(self,value):
	if abs(value)>255:
	    value = 255 if (value>0) else -255
	self.__speed = int(value)
	self.__thread = threading.Thread(target=self.run_motor)
	self.__thread.setDaemon('True')
	self.__thread.start()

 
    ## Stop running the motor.
    def off(self):
        self.__speed = 0
	self.__thread = None
    # Set the current rotation speed of the motor to a given speed
    def update_speed(self,speed):
	if abs(speed) > 255:
	    speed = 255 if (speed >0) else -255
	self.__speed = int(speed)
    ## TO DO: Example on
        ## https://github.com/DexterInd/BrickPi_Python/blob/master/Sensor_Examples/BrickPi.py
    def rotate_angle(self):
        pass

   

## 
## A superclass concerning sensors (both the GPIO and the LEGO-MINDSTORM)
##
class Sensor:
    def __init__(self,nb_values):
        self.__value = []
	self.__nb_values = nb_values
	self.__going = False
	self.__thread = None
    def update_value(self):
        pass
    def add_value(self,value):
	while (len(self.__value) >= self.__nb_values):
	     self.__value.pop(0)
	self.__value.append(value)
    def going(self):
	return self.__going
    def get_value(self):
	try:
	    copy = sorted(self.__value)
	    while copy[0] == None:
		copy.pop(0)
	    return copy[len(copy)/2]
	except:
	    return None       
    def on(self):
	self.__going = True
	self.__thread = threading.Thread(target=self.update_value)
	self.__thread.setDaemon(True)
	self.__thread.start()
    def off(self):
	self.__run = False
	self.__thread = None
##
## A class to get the value of the distance sensor.
## Code conform Hands-on tutorial raspberry pi
## 
class DistanceSensor(Sensor):
    def __init__(self,echo_gpio,trig_gpio):
	Sensor.__init__(self,5)
        self.__echo_gpio = echo_gpio
        self.__trig_gpio = trig_gpio
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(echo_gpio, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        GPIO.setup(trig_gpio, GPIO.OUT)
        GPIO.output(trig_gpio,False)
    def update_value(self):
        trig_duration = 0.0001
        inttimeout = 2100
        v_snd = 340.29
	while self.going():
	    GPIO.output(self.__trig_gpio,True)
       	    time.sleep(trig_duration)
	    GPIO.output(self.__trig_gpio,False)
       	    count_high = inttimeout
	    while ( GPIO.input(self.__echo_gpio) == 0 and count_high >0):
        	count_high -= 1
	    if count_high > 0:
                echo_start = time.time()
                count_low = inttimeout
                while ( GPIO.input(self.__echo_gpio) == 1 and count_low >0):
                    count_low -= 1
                echo_end = time.time()
                echo_duration = echo_end - echo_start
            if count_high>0 and count_low >0:
                distance = echo_duration * v_snd *100./2.
                self.add_value(distance)
	    else:
                self.add_value(None)
	    time.sleep(0.1)

class MindstormSensor(Sensor):
    def __init__(self,port,sensor_type):
	Sensor.__init__(self,3)
	self.__port = port
	exec('BrickPi.SensorType[PORT_'+str(self.__port)+'] = TYPE_SENSOR_'+ sensor_type)
    def update_value(self):
	while self.going():
	     BrickPiUpdateValues()
	     exec('value = BrickPi.Sensor[PORT_'+ str(self.__port) +']')
	     print 'a' + str(value)
	     self.add_value(value)
	     time.sleep(0.1)
	
