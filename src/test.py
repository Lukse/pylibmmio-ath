import sys
import time
sys.path.append("/usr/sbin")
import mmio_lib_ath
import libmmio

print 'GPIO blinking'


iomem = libmmio.mmiof_init(0x18040000) 				# GPIO base address
libmmio.mmiof_write(iomem, 0x00, 0x00046cff) 		# Set gpio direction

while True:
	libmmio.mmiof_write(iomem, 0x0C, 0x00042605) 	# Set GPIO registers
	time.sleep(1)

	libmmio.mmiof_write(iomem, 0x10, 0x00042605) 	# Clear GPIO registers
	time.sleep(1) 
