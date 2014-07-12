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
#sys.path.append("/usr/sbin") # this is where binary library and python wrapper resides
import libmmio

class GPIO:
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


class I2C:
	def __init__(self, scl_pin=18, sda_pin=19, frequency=0):
		self.gpio = GPIO()
		self.scl_pin = scl_pin
		self.sda_pin = sda_pin
		self.sleep = frequency
		self.gpio.pin_set(self.sda_pin) 
		self.gpio.pin_set(self.scl_pin) 
		self.gpio.pin_direction(self.scl_pin, self.gpio.OUTPUT)
		self.gpio.pin_direction(self.sda_pin, self.gpio.OUTPUT)


	def start(self):
		self.gpio.pin_set(self.sda_pin) 
		time.sleep(self.sleep)

		self.gpio.pin_set(self.scl_pin) 
		time.sleep(self.sleep)
		
		self.gpio.pin_clear(self.sda_pin) 
		time.sleep(self.sleep)
		
		self.gpio.pin_clear(self.scl_pin) 
		time.sleep(self.sleep)


	def stop(self):
		self.gpio.pin_clear(self.sda_pin)
		time.sleep(self.sleep)
		
		self.gpio.pin_set(self.scl_pin)
		time.sleep(self.sleep)

		self.gpio.pin_set(self.sda_pin)
		time.sleep(self.sleep)


	def write(self, d):
		for x in xrange(8):
			if d & 0x80:
				self.gpio.pin_set(self.sda_pin) 
			else:
				self.gpio.pin_clear(self.sda_pin) 
			
			self.gpio.pin_set(self.scl_pin)
			time.sleep(self.sleep)
			self.gpio.pin_clear(self.scl_pin)
			time.sleep(self.sleep)
			d = d << 1
		
		self.gpio.pin_clear(self.sda_pin)
		self.gpio.pin_direction(self.sda_pin, self.gpio.INPUT)
		time.sleep(self.sleep)

		self.gpio.pin_set(self.scl_pin)
		time.sleep(self.sleep)

		ack = self.gpio.pin_read(self.sda_pin)
		self.gpio.pin_clear(self.scl_pin)

		self.gpio.pin_direction(self.sda_pin, self.gpio.OUTPUT)
		self.gpio.pin_clear(self.sda_pin)
		time.sleep(self.sleep)
		
		return ack


	def read(self, ack):
		d = 0
		self.gpio.pin_direction(self.sda_pin, self.gpio.INPUT)

		for x in xrange(8):
			time.sleep(self.sleep)
			self.gpio.pin_set(self.scl_pin)
			time.sleep(self.sleep)
			d = d << 1
			if(self.gpio.pin_read(self.sda_pin)):
				d = d | 1
			time.sleep(self.sleep)
			self.gpio.pin_clear(self.scl_pin)

		self.gpio.pin_direction(self.sda_pin, self.gpio.OUTPUT)
		time.sleep(self.sleep)

		if ack == True:
			self.gpio.pin_clear(self.sda_pin)
		else:
			self.gpio.pin_set(self.sda_pin)
		time.sleep(self.sleep)

		self.gpio.pin_set(self.scl_pin)
		time.sleep(self.sleep)

		self.gpio.pin_clear(self.scl_pin)
		time.sleep(self.sleep)
		return d


class SPI:
	def __init__(self, MOSI_pin=19, MISO_pin=19, CLOCK_pin=18, SS_pin=20, frequency=0):
		self.gpio = GPIO()

		self.MOSI_pin=MOSI_pin
		self.MISO_pin=MISO_pin
		self.CLOCK_pin=CLOCK_pin
		self.SS_pin=SS_pin
		self.sleep = frequency

		self.gpio.pin_set(self.MOSI_pin) 
		self.gpio.pin_set(self.MISO_pin) 
		self.gpio.pin_set(self.CLOCK_pin) 
		self.gpio.pin_set(self.SS_pin) 

		self.gpio.pin_direction(self.MISO_pin, self.gpio.INPUT)
		self.gpio.pin_direction(self.MOSI_pin, self.gpio.OUTPUT)
		self.gpio.pin_direction(self.CLOCK_pin, self.gpio.OUTPUT)
		self.gpio.pin_direction(self.SS_pin, self.gpio.OUTPUT)

	def start(self):
		self.gpio.pin_clear(self.SS_pin)
		time.sleep(self.sleep)


	def stop(self):
		time.sleep(self.sleep)
		self.gpio.pin_set(self.SS_pin)


	def transfer(self, data):
		# CPHA = 1  even clock changes are used to sample the data 
		# CPOL = 0  active-Hi clock 
		
		read = 0
		for x in xrange(8):
			time.sleep(self.sleep)
			self.gpio.pin_direction(self.MOSI_pin, self.gpio.OUTPUT) # in this case it's single line comunication
			time.sleep(self.sleep)

			if data & 0x80:
				self.gpio.pin_set(self.MOSI_pin) 
			else:
				self.gpio.pin_clear(self.MOSI_pin) 
			
			data = data << 1

			time.sleep(self.sleep)
			self.gpio.pin_clear(self.CLOCK_pin) 
			time.sleep(self.sleep)
			
			self.gpio.pin_direction(self.MISO_pin, self.gpio.INPUT) # in this case it's single line comunication
			time.sleep(self.sleep)
			self.gpio.pin_set(self.CLOCK_pin) 			
			time.sleep(self.sleep)

			read = read << 1
			if(self.gpio.pin_read(self.MISO_pin)):
				read = read | 1

		return read















class HD44780:  
	def __init__(self, RS_pin=23, E_pin=22, DATA_pin=[21, 20, 19, 18]):
		self.gpio = GPIO()

		self.RS_pin=RS_pin
		self.E_pin=E_pin
		self.DATA_pin=DATA_pin

		self.gpio.pin_direction(self.RS_pin, self.gpio.OUTPUT)
		self.gpio.pin_direction(self.E_pin, self.gpio.OUTPUT)
		self.gpio.pin_direction(self.DATA_pin[0], self.gpio.OUTPUT)
		self.gpio.pin_direction(self.DATA_pin[1], self.gpio.OUTPUT)
		self.gpio.pin_direction(self.DATA_pin[2], self.gpio.OUTPUT)
		self.gpio.pin_direction(self.DATA_pin[3], self.gpio.OUTPUT)

		self.clear()  

	def pin(self, pin, value):
		if value == True:
			self.gpio.pin_set(pin)
		else:
			self.gpio.pin_clear(pin)


	def clear(self):  
		""" Blank / Reset LCD """  

		self.cmd(0x33) # $33 8-bit mode  
		self.cmd(0x32) # $32 8-bit mode  
		self.cmd(0x28) # $28 8-bit mode  
		self.cmd(0x0C) # $0C 8-bit mode  
		self.cmd(0x06) # $06 8-bit mode  
		self.cmd(0x01) # $01 8-bit mode  

	def cmd(self, bits, char_mode=False):  
		""" Send command to LCD """  

		time.sleep(0.001)  
		bits=bin(bits)[2:].zfill(8)  

		#gpio.write(self.RS_pin, char_mode)
		self.pin(self.RS_pin, char_mode)

		for pin in self.DATA_pin:  
			#gpio.write(pin, False)  
			self.pin(pin, False)

		for i in range(4):  
			if bits[i] == "1":  
				#gpio.write(self.DATA_pin[::-1][i], True)  
				self.pin(self.DATA_pin[::-1][i], True)

		#gpio.write(self.E_pin, True)  
		self.pin(self.E_pin, True)
		
		#gpio.write(self.E_pin, False)  
		self.pin(self.E_pin, False)

		for pin in self.DATA_pin:  
			#gpio.write(pin, False)  
			self.pin(pin, False)

		for i in range(4,8):  
			if bits[i] == "1":  
				#gpio.write(self.DATA_pin[::-1][i-4], True)  
				self.pin(self.DATA_pin[::-1][i-4], True)  

		#gpio.write(self.E_pin, True)  
		self.pin(self.E_pin, True)
		#gpio.write(self.E_pin, False)  
		self.pin(self.E_pin, False)  

	def message(self, text):  
		""" Send string to LCD. Newline wraps to second line"""  

		for char in text:  
			if char == '\n':  
				self.cmd(0xC0) # next line  
			else:  
				self.cmd(ord(char),True)  
  
