import time;
from machine import Pin, UART;
uart = UART(0, baudrate=115200, tx=Pin(12), rx=Pin(13))
uart.init(bits=8, parity=None, stop=2)
button = Pin(0, Pin.IN, Pin.PULL_DOWN);
button0 = Pin(0, Pin.IN, Pin.PULL_DOWN); button1 = Pin(1, Pin.IN, Pin.PULL_DOWN); button2 = Pin(2, Pin.IN, Pin.PULL_DOWN); button3 = Pin(3, Pin.IN, Pin.PULL_DOWN); button4 = Pin(4, Pin.IN, Pin.PULL_DOWN); button5 = Pin(5, Pin.IN, Pin.PULL_DOWN); button6 = Pin(6, Pin.IN, Pin.PULL_DOWN); button7 = Pin(7, Pin.IN, Pin.PULL_DOWN); button8 = Pin(8, Pin.IN, Pin.PULL_DOWN); button9 = Pin(9, Pin.IN, Pin.PULL_DOWN); button10 = Pin(10, Pin.IN, Pin.PULL_DOWN);


while True:
    if button0.value() == 1:
    	print("1 pressed")
    	uart.write(bytes([0x01]))
    elif button1.value() == 1:
        print("2 pressed")
        uart.write(bytes([0x02]))
    elif button2.value() == 1:
    	print("3 pressed")
    	uart.write(bytes([0x03]))
    elif button3.value() == 1:
        print("4 pressed")
        uart.write(bytes([0x04]))
    elif button4.value() == 1:
    	print("5 pressed")
    	uart.write(bytes([0x05]))
    elif button5.value() == 1:
        print("6 pressed")
        uart.write(bytes([0x06]))
    elif button7.value() == 1:
    	print("7 pressed")
    	uart.write(bytes([0x07]))
    elif button8.value() == 1:
        print("8 pressed")
        uart.write(bytes([0x08]))
    elif button9.value() == 1:
    	print("9 pressed")
    	uart.write(bytes([0x09]))
    elif button10.value() == 1:
        print("10 pressed")
        uart.write(bytes([0x0a]))
    else: 
        print("no button pressed")
        uart.write(bytes([0x00]))
    time.sleep(0.2)
