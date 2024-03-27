import time;
import serial
import RPi.GPIO as GPIO

ser = serial.Serial('/dev/ttyS0') 
ser.baudrate = 115200

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)

try:
   while True:
      x = ser.read(3)
      print(x)
      if x == b'\x01\x0a\x0d':
        GPIO.output(23,True)
      elif x == b'\x02\x0a\x0d':
        GPIO.output(23,True)
      else:
        GPIO.output(23,False)
      
      time.sleep(0.175)

finally:
   GPIO.output(23,False)
   GPIO.cleanup()
