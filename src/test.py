import sys
import time
sys.path.append("/usr/sbin") # this is where binary library and python wrapper resides
import hwlibcara2


# ---------
# GPIO test
# ---------
gpio = hwlibcara2.GPIO()
gpio.pin_direction(12, gpio.OUTPUT)
gpio.pin_set(12)
print gpio.pin_read(11) # push button near USB connector


# --------
# I2C test
# --------
i2c = hwlibcara2.I2C(frequency=0)

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

