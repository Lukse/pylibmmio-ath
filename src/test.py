import sys
import time
sys.path.append("/usr/sbin") # this is where binary library and python wrapper resides
import hwlibcara2



# ---------
# GPIO test
# ---------
gpio = hwlibcara2.GPIO()
gpio.pin_direction(12, 1)
gpio.pin_set(12)
while True:
	gpio.pin_set(12)
	print gpio.pin_read(11) # push button near USB connector
	time.sleep(0.1)
	gpio.pin_clear(12)
	time.sleep(0.1)


'''
# --------
# I2C test
# detect devices on line
# add 10k pullup on SDA pin
# --------
i2c = hwlibcara2.I2C()

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
'''

'''
# --------
# I2C test
# PCF8575
# add 10k pullup on SDA pin
# --------
i2c = hwlibcara2.I2C()

# input
i2c.start()
i2c.write(0x41)
print i2c.read(True)
print i2c.read(False)
i2c.stop()

# output
i2c.start()
i2c.write(0x40)
i2c.write(0x55)
i2c.write(0xAA)
i2c.stop()
'''

'''
# --------
# SPI test
# MLX90316
# --------
spi = hwlibcara2.SPI()

while True:
	spi.start()
	spi.transfer(0xAA)
	spi.transfer(0xFF)
	d0 = spi.transfer(0xFF)
	d1 = spi.transfer(0xFF)
	d2 = spi.transfer(0xFF)
	d3 = spi.transfer(0xFF)
	spi.transfer(0xFF)
	spi.transfer(0xFF)
	spi.transfer(0xFF)
	spi.transfer(0xFF)
	spi.stop()

	#print "%3.2f" % (((d0*0x100 + d1)&0xFFFC >> 2) * 359.999 / 0x3FFF)
	#print "0x%04X" % (((d0*0x100 | d1) & 0xFFFC) >> 2) 
	print "0x%02X" % d0, 
	print "0x%02X" % d1
'''

'''
# --------
# SPI test
# MLX90316
# --------
lcd = hwlibcara2.HD44780()
lcd.message('Python inside')
'''