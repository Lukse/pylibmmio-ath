# -*- coding: utf-8 -*-
#
# Copyright (C) 2014 Saulius Lukšė 
# See LICENSE for more information.
#

'''
Carambola2 motherboard
=====================================
   usb   USB   button   reset

1	UART_TX				1	LED6
2	UART_RX				2	LED5
3	UART_TX_C			3	LED4
4	UART_RX_C			4	LED3
5	GND					5	LED2
6	USB+				6	LED1
7	USB-				7	LED0
8	USB+C				8	GPIO11 (button)
9	USB-C				9	GPIO12
10	GND					10	GPIO18
11	SPI_CS				11	GPIO19
12	SPI_CLK				12	GPIO20
13	SPI_MOSI			13	GPIO21
14	SPI_MISO			14	GPIO22
15	RESET				15	GPIO23
16	3.3V				16	3.3V
17	3.3V				17	3.3V
18	5V					18	5V
19	5V					19	5V
20	GND					20	GND
            
            LAN LAN
'''


import sys
import time
sys.path.append("/usr/sbin") # this is where binary library and python wrapper resides
import libmmio

class CARAMBOLA2_GPIO:
	def __init__(self):
		self.GPIO_BASE					= 0x18040000
		self.GPIO_OE					= 0x00 		# General Purpose I/O Output Enable page 65
		self.GPIO_IN					= 0x04 		# General Purpose I/O Input Value page 65
		self.GPIO_OUT					= 0x08 		# General Purpose I/O Output Value page 65
		self.GPIO_SET					= 0x0C 		# General Purpose I/O Bit Set page 66
		self.GPIO_CLEAR					= 0x10 		# General Purpose I/O Per Bit Clear page 66
		self.GPIO_INT					= 0x14 		# General Purpose I/O Interrupt Enable page 66
		self.GPIO_INT_TYPE				= 0x18 		# General Purpose I/O Interrupt Type page 66
		self.GPIO_INT_POLARITY			= 0x1C 		# General Purpose I/O Interrupt Polarity page 66
		self.GPIO_INT_PENDING			= 0x20 		# General Purpose I/O Interrupt Pending page 67
		self.GPIO_INT_MASK				= 0x24 		# General Purpose I/O Interrupt Mask page 67
		self.GPIO_FUNCTION_1			= 0x28 		# General Purpose I/O Function page 67
		self.GPIO_IN_ETH_SWITCH_LED		= 0x2C 		# General Purpose I/O Input Value page 68
		self.GPIO_FUNCTION_2			= 0x30 		# Extended GPIO Function Control page 69

		self.INPUT = 0
		self.OUTPUT = 1

		self.iomem = None

		ALL_PINS = [11, 12, 18, 19, 20, 21, 22, 23]

		#ALL_GPIO = 1<<11 | 1<<12 | 1<<18 | 1<<19 | 1<<20 | 1<<21 | 1<<22 | 1<<23
		self.iomem = libmmio.mmiof_init(self.GPIO_BASE) 				# GPIO base address
		pin_status = libmmio.mmiof_read(self.iomem, self.GPIO_OE)
		
		# set all pins as input
		for pin in ALL_PINS:
			pin_status  &= ~(1 << pin);

		libmmio.mmiof_write(self.iomem, self.GPIO_OE, pin_status) 		# Set gpio direction
		libmmio.mmiof_write(self.iomem, self.GPIO_FUNCTION_2, 1<<8 | 1<<9) 	# Disables the WPS input function on GPIO12, Disables Jumpstart input function on GPIO11


	def pin_direction(self, bit, direction):
		if 11 <= bit <= 23:
			pin_status = libmmio.mmiof_read(self.iomem, self.GPIO_OE)

			if direction == 1:
				pin_status |= 1 << bit;
			
			elif direction == 0:
				pin_status  &= ~(1 << bit);				

			libmmio.mmiof_write(self.iomem, self.GPIO_OE, pin_status)

		else:
			raise Exception("PIN number not in valid range.")

		
	def pin_set(self, bit):
		if 11 <= bit <= 23:
			libmmio.mmiof_write(self.iomem, self.GPIO_SET, 1<<bit)
		else:
			raise Exception("PIN number not in valid range.")


	def pin_clear(self, bit):
		if 11 <= bit <= 23:
			libmmio.mmiof_write(self.iomem, self.GPIO_CLEAR, 1<<bit)
		else:
			raise Exception("PIN number not in valid range.")


	def pin_read(self, bit):
		if 11 <= bit <= 23:
			pin_status = libmmio.mmiof_read(self.iomem, self.GPIO_IN)
			if (pin_status & 1<<bit) != 0:
				return True
			else:
				return False
		else:
			raise Exception("PIN number not in valid range.")




gpio = CARAMBOLA2_GPIO()

gpio.pin_direction(12, gpio.OUTPUT)

'''
while True:
	gpio.pin_set(12) 
	time.sleep(0.1)

	gpio.pin_clear(12) 
	time.sleep(0.1)

	print gpio.pin_read(11)
'''



# =================================

class I2C:
	def __init__(self, gpio, scl_pin=18, sda_pin=19, frequency=0):
		self.gpio = gpio
		self.scl_pin = scl_pin
		self.sda_pin = sda_pin
		self.sleep = frequency
		gpio.pin_set(self.sda_pin) 
		gpio.pin_set(self.scl_pin) 
		self.gpio.pin_direction(self.scl_pin, gpio.OUTPUT)
		self.gpio.pin_direction(self.sda_pin, gpio.OUTPUT)
		#time.sleep(0.2)


	def start(self):
		gpio.pin_set(self.sda_pin) 
		time.sleep(self.sleep)

		gpio.pin_set(self.scl_pin) 
		time.sleep(self.sleep)
		
		gpio.pin_clear(self.sda_pin) 
		time.sleep(self.sleep)
		
		gpio.pin_clear(self.scl_pin) 
		time.sleep(self.sleep)


	def stop(self):
		gpio.pin_clear(self.sda_pin)
		time.sleep(self.sleep)
		
		gpio.pin_set(self.scl_pin)
		time.sleep(self.sleep)

		gpio.pin_set(self.sda_pin)
		time.sleep(self.sleep)


	def write(self, d):
		for x in xrange(8):
			if d & 0x80:
				gpio.pin_set(self.sda_pin) 
			else:
				gpio.pin_clear(self.sda_pin) 
			
			gpio.pin_set(self.scl_pin)
			time.sleep(self.sleep)
			gpio.pin_clear(self.scl_pin)
			time.sleep(self.sleep)
			d = d << 1
		
		gpio.pin_clear(self.sda_pin)
		self.gpio.pin_direction(self.sda_pin, gpio.INPUT)
		time.sleep(self.sleep)

		gpio.pin_set(self.scl_pin)
		time.sleep(self.sleep)

		ack = self.gpio.pin_read(self.sda_pin)
		gpio.pin_clear(self.scl_pin)

		self.gpio.pin_direction(self.sda_pin, gpio.OUTPUT)
		gpio.pin_clear(self.sda_pin)
		time.sleep(self.sleep)
		
		return ack


	def read(self, ack):
		d = 0
		self.gpio.pin_direction(self.sda_pin, gpio.INPUT)

		for x in xrange(8):
			time.sleep(self.sleep)
			gpio.pin_set(self.scl_pin)
			time.sleep(self.sleep)
			d = d << 1
			if(self.gpio.pin_read(self.sda_pin)):
				d = d | 1
			time.sleep(self.sleep)
			gpio.pin_clear(self.scl_pin)

		self.gpio.pin_direction(self.sda_pin, gpio.OUTPUT)
		time.sleep(self.sleep)

		if ack == True:
			gpio.pin_clear(self.sda_pin)
		else:
			gpio.pin_set(self.sda_pin)
		time.sleep(self.sleep)

		gpio.pin_set(self.scl_pin)
		time.sleep(self.sleep)

		gpio.pin_clear(self.scl_pin)
		time.sleep(self.sleep)
		return d


i2c = I2C(gpio, frequency=0)

# scan
for i in xrange(255):
	i2c.start()
	ack = i2c.write(i)
	if not ack:
		if i & 0x01:
			print "R 0x%02X" % i
		else:
			print "W 0x%02X" % i
	i2c.stop()



#print
#i2c.start()
#i2c.write(0x41)
#print i2c.read(True)
#print i2c.read(False)
#i2c.stop()

#i2c.start()
#i2c.write(64)
#i2c.write(0x55)
#i2c.write(0xAA)
#i2c.stop()

i2c.start()
i2c.write(0xE0)
i2c.write(0x00)
i2c.write(0x51)
i2c.stop()

time.sleep(0.2)

i2c.start()
i2c.write(0xE0)
i2c.write(0x02)
i2c.stop()

i2c.start()
i2c.write(0xE1)
d1 = i2c.read(True)
d2 = i2c.read(False)
i2c.stop()

print d1, d2

