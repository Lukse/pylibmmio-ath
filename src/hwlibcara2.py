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
		self.iomem = None

		ALL_PINS = [11, 12, 18, 19, 20, 21, 22, 23]

		self.iomem = libmmio.mmiof_init(libmmio.GPIO_BASE) 				# GPIO base address
		pin_status = libmmio.mmiof_read(self.iomem, libmmio.GPIO_OE)
		
		# set all pins as input
		for pin in ALL_PINS:
			self.pin_direction(pin, libmmio.INPUT)
		libmmio.mmiof_write(self.iomem, libmmio.GPIO_OE, pin_status) 		# Set gpio direction

		# Disable the WPS input function on GPIO12, Disables Jumpstart input function on GPIO11
		libmmio.mmiof_write(self.iomem, libmmio.GPIO_FUNCTION_2, 1<<8 | 1<<9) 	


	def pin_direction(self, bit, direction):
		# TODO: range checking
		libmmio.pin_direction(self.iomem, bit, direction)

		
	def pin_set(self, bit):
		# TODO: range checking
		libmmio.pin_set(self.iomem, bit)


	def pin_clear(self, bit):
		# TODO: range checking
		libmmio.pin_clear(self.iomem, bit)


	def pin_read(self, bit):
		 # TODO: how to return boolean from C?
		if libmmio.pin_read(self.iomem, bit) == 1:
			return True
		else:
			return False


class I2C:
	def __init__(self, scl_pin=18, sda_pin=19, frequency=0):
		self.gpio = GPIO()
		self.scl_pin = scl_pin
		self.sda_pin = sda_pin
		self.sleep = frequency
		self.gpio.pin_set(self.sda_pin) 
		self.gpio.pin_set(self.scl_pin) 
		self.gpio.pin_direction(self.scl_pin, libmmio.OUTPUT)
		self.gpio.pin_direction(self.sda_pin, libmmio.OUTPUT)


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
		self.gpio.pin_direction(self.sda_pin, libmmio.INPUT)
		time.sleep(self.sleep)

		self.gpio.pin_set(self.scl_pin)
		time.sleep(self.sleep)

		ack = self.gpio.pin_read(self.sda_pin)
		self.gpio.pin_clear(self.scl_pin)

		self.gpio.pin_direction(self.sda_pin, libmmio.OUTPUT)
		self.gpio.pin_clear(self.sda_pin)
		time.sleep(self.sleep)
		
		return ack


	def read(self, ack):
		d = 0
		self.gpio.pin_direction(self.sda_pin, libmmio.INPUT)

		for x in xrange(8):
			time.sleep(self.sleep)
			self.gpio.pin_set(self.scl_pin)
			time.sleep(self.sleep)
			d = d << 1
			if(self.gpio.pin_read(self.sda_pin)):
				d = d | 1
			time.sleep(self.sleep)
			self.gpio.pin_clear(self.scl_pin)

		self.gpio.pin_direction(self.sda_pin, libmmio.OUTPUT)
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

		self.gpio.pin_direction(self.MISO_pin, libmmio.INPUT)
		self.gpio.pin_direction(self.MOSI_pin, libmmio.OUTPUT)
		self.gpio.pin_direction(self.CLOCK_pin, libmmio.OUTPUT)
		self.gpio.pin_direction(self.SS_pin, libmmio.OUTPUT)

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
			self.gpio.pin_direction(self.MOSI_pin, libmmio.OUTPUT) # in this case it's single line comunication
			time.sleep(self.sleep)

			if data & 0x80:
				self.gpio.pin_set(self.MOSI_pin) 
			else:
				self.gpio.pin_clear(self.MOSI_pin) 
			
			data = data << 1

			time.sleep(self.sleep)
			self.gpio.pin_clear(self.CLOCK_pin) 
			time.sleep(self.sleep)
			
			self.gpio.pin_direction(self.MISO_pin, libmmio.INPUT) # in this case it's single line comunication
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

		self.gpio.pin_direction(self.RS_pin, libmmio.OUTPUT)
		self.gpio.pin_direction(self.E_pin, libmmio.OUTPUT)
		self.gpio.pin_direction(self.DATA_pin[0], libmmio.OUTPUT)
		self.gpio.pin_direction(self.DATA_pin[1], libmmio.OUTPUT)
		self.gpio.pin_direction(self.DATA_pin[2], libmmio.OUTPUT)
		self.gpio.pin_direction(self.DATA_pin[3], libmmio.OUTPUT)

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
  
