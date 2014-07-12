/*
 * Copyright (C) 2012 Žilvinas Valinskas, Saulius Lukšė
 * See LICENSE for more information.
 */

// TODO: Clean up code

#include <sys/mman.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <errno.h>
#include <fcntl.h>
#include "mmio.h"
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <stdbool.h>

#define GPIO_BASE					0x18040000 // GPIO base address
#define GPIO_OE						0x00 		// General Purpose I/O Output Enable page 65
#define GPIO_IN						0x04 		// General Purpose I/O Input Value page 65
#define GPIO_OUT					0x08 		// General Purpose I/O Output Value page 65
#define GPIO_SET					0x0C 		// General Purpose I/O Bit Set page 66
#define GPIO_CLEAR					0x10 		// General Purpose I/O Per Bit Clear page 66
#define GPIO_INT					0x14 		// General Purpose I/O Interrupt Enable page 66
#define GPIO_INT_TYPE				0x18 		// General Purpose I/O Interrupt Type page 66
#define GPIO_INT_POLARITY			0x1C 		// General Purpose I/O Interrupt Polarity page 66
#define GPIO_INT_PENDING			0x20 		// General Purpose I/O Interrupt Pending page 67
#define GPIO_INT_MASK				0x24 		// General Purpose I/O Interrupt Mask page 67
#define GPIO_FUNCTION_1				0x28 		// General Purpose I/O Function page 67
#define GPIO_IN_ETH_SWITCH_LED		0x2C 		// General Purpose I/O Input Value page 68
#define GPIO_FUNCTION_2				0x30 		// Extended GPIO Function Control page 69

#define INPUT 						0
#define OUTPUT 						1

static inline uint32_t readl(void *ptr)
{
	uint32_t *data = ptr;
	return *data;
}

static inline void writel(uint32_t value, void *ptr)
{
	uint32_t *data = ptr;
	*data = value;
}

static void mmio_normalize(struct mmio *mo)
{
	int npages = 0;

	mo->iobase += mo->offset;
	mo->offset = mo->iobase & (getpagesize() - 1);
	mo->iobase = mo->iobase & ~(getpagesize() - 1);

	npages += (mo->range * sizeof(uint32_t)) / getpagesize();
	npages += 1;
	mo->iosize = npages * getpagesize();
}

static void mmio_init(struct mmio *mo)
{
	char *device;
	int iofd;

	if (!mo->kmem)
		device = "/dev/mem";
	else
		device = "/dev/kmem";

	iofd = open(device, O_RDWR);
	if (iofd < 0)
	{
		//ie_errno("open() failed");
		printf("open failed\n");
		exit(-1);
		// TODO:
	}

	mo->iomem = mmap(NULL, mo->iosize,
			 PROT_READ|PROT_WRITE,
			 MAP_SHARED,
			 iofd, mo->iobase);

	if (mo->iomem == MAP_FAILED)
	{
		printf("can't map\n");
		exit(-1);
		//die_errno("can't map @ %0lX", mo->iobase);
	}

	close(iofd);
}

void * mmiof_init(unsigned long iobase)
{
	struct 			mmio io1;
	unsigned long 	offset;
	unsigned long 	range;
	size_t			iosize;
	void			*iomem;
	range  = 0;

	int npages = 0;

	offset = iobase & (getpagesize() - 1);
	iobase = iobase & ~(getpagesize() - 1);

	npages += (range * sizeof(uint32_t)) / getpagesize();
	npages += 1;
	iosize = npages * getpagesize();

	char *device;
	int iofd;

	device = "/dev/mem";
	//device = "/dev/kmem";

	iofd = open(device, O_RDWR);
	if (iofd < 0)
	{
		//ie_errno("open() failed");
		printf("open failed\n");
		exit(-1);
		// TODO:
	}

	iomem = mmap(NULL, iosize, PROT_READ|PROT_WRITE, MAP_SHARED, iofd, iobase);

	if (iomem == MAP_FAILED)
	{
		printf("can't map\n");
		exit(-1);
		//die_errno("can't map @ %0lX", mo->iobase);
	}

	close(iofd);	
	return iomem;

}

unsigned long mmiof_read(void * iomem, unsigned long offset)
{
	void *addr;
	addr = iomem + offset;
	unsigned long read_data = readl(addr);
	return read_data;
}

void mmiof_write(void * iomem, unsigned long offset, unsigned long value)
{
	void *addr;
	addr = iomem + offset;
	uint32_t *data = addr;
	*data = value;
}

void mmiof_close(void * iomem)
{
	if (munmap(iomem, 4096))
	{
		exit(-1);
		//die_errno("can't unmap @ %lX", io->iobase);
	}
}







// --------------------------------------------------------------------------------
// --------------------------- higher level functions -----------------------------
// --------------------------------------------------------------------------------


// --------------------------------------------------------------------------------
// GPIO functions

void pin_set(void * iomem, unsigned int bit)
{
	mmiof_write(iomem, GPIO_SET, 1 << bit);
}

void pin_clear(void * iomem, unsigned int bit)
{
	mmiof_write(iomem, GPIO_CLEAR, 1 << bit);
}

unsigned int pin_read(void * iomem, unsigned int bit)
{
	return (mmiof_read(iomem, GPIO_IN) & (1 << bit)) >> bit;
}

void pin_direction(void * iomem, unsigned int bit, unsigned int direction)
{
	unsigned long int pin_status = mmiof_read(iomem, GPIO_OE);

	if (direction == 1)
		pin_status |= 1 << bit;
	else
		pin_status  &= ~(1 << bit);

	mmiof_write(iomem, GPIO_OE, pin_status);
}

// --------------------------------------------------------------------------------
// I2C functions
















void * test_get_buffer(void)
{	
	return "1234567890";
}

void test_put_buffer(char * buffer)
{
	printf("C prints: %s\n", buffer);
}


