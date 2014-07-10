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
sys.path.append("/usr/sbin")
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

		INPUT = 0
		OUTPUT = 1

		self.iomem = None

		ALL_PINS = [11, 12, 18, 19, 20, 21, 22, 23]

		#ALL_GPIO = 1<<11 | 1<<12 | 1<<18 | 1<<19 | 1<<20 | 1<<21 | 1<<22 | 1<<23
		self.iomem = libmmio.mmiof_init(self.GPIO_BASE) 				# GPIO base address
		pin_status = libmmio.mmiof_read(self.iomem, self.GPIO_OE)
		
		# set all pins as input
		for pin in ALL_PINS:
			pin_status  &= ~(1 << pin);

		libmmio.mmiof_write(self.iomem, self.GPIO_OE, pin_status) 		# Set gpio direction


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

gpio.pin_direction(11, 1)

while True:
	gpio.pin_set(11) 
	time.sleep(0.1)

	gpio.pin_clear(11) 
	time.sleep(0.1)

	print gpio.pin_read(12)


'''


ALL_GPIO = 1<<11 | 1<<12 | 1<<18 | 1<<19 | 1<<20 | 1<<21 | 1<<22 | 1<<23


print 'GPIO blinking'

iomem = libmmio.mmiof_init(GPIO_BASE) 				# GPIO base address
libmmio.mmiof_write(iomem, GPIO_OE, ALL_GPIO) 		# Set gpio direction

libmmio.mmiof_write(iomem, GPIO_FUNCTION_2, 1<<8 | 1<<9) 	# Disables the WPS input function on GPIO12, Disables Jumpstart input function on GPIO11

print 'GPIO_FUNCTION_2: ', libmmio.mmiof_read(iomem, GPIO_FUNCTION_2)

print "Python prints", libmmio.cdata(libmmio.test_get_buffer(), 6)
libmmio.test_put_buffer('9876543210')

while True:
	libmmio.mmiof_write(iomem, GPIO_SET, ALL_GPIO) 	# Set GPIO registers
	time.sleep(0.1)

	libmmio.mmiof_write(iomem, GPIO_CLEAR, ALL_GPIO) 	# Clear GPIO registers
	time.sleep(0.1) 

'''
