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

uint32_t mmio_readl(const struct mmio *io, unsigned int offset)
{
	void *addr;

	addr = io->iomem + io->offset + offset;
	return readl(addr);
}

void mmio_writel(const struct mmio *io, unsigned int offset, uint32_t value)
{
	void *addr;

	addr = io->iomem + io->offset + offset;
	writel(value, addr);
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

int mmio_map(struct mmio *io, unsigned long base, size_t length)
{
	memset(io, 0, sizeof(*io));

	io->iobase = base;
	io->offset = 0;
	io->range  = length;

	mmio_normalize(io);
	mmio_init(io);

	return 0;
}

void mmio_unmap(struct mmio *io)
{
	if (munmap(io->iomem, io->iosize))
	{
		exit(-1);
		//die_errno("can't unmap @ %lX", io->iobase);
	}

	memset(io, 0, sizeof(*io));
}

void mmio_hexdump(const struct mmio *io, size_t length, size_t flags)
{
	__hexdump(io->iobase + io->offset,
		  io->iomem + io->offset,
		  length, flags);
}

unsigned long mmio_read(unsigned long iobase)
{
    struct mmio io;
    uint32_t rdata;

    mmio_map(&io, iobase, 0);
    rdata = mmio_readl(&io, 0);
    mmio_unmap(&io);
    return rdata;
}

unsigned long mmio_write(unsigned long iobase, unsigned long data2)
{
    struct mmio io;
    uint32_t data;

    mmio_map(&io, iobase, 0);
    mmio_writel(&io, 0, data2);
    data = mmio_readl(&io, 0);
    mmio_unmap(&io);
    if (data != data2)
        return -1;
    else
        return 0;
}

unsigned long mmio_write2(unsigned long iobase, unsigned long data2)
{
    struct mmio io;
    uint32_t data;

    mmio_map(&io, iobase, 0);
    mmio_writel(&io, 0, data2);
    data = mmio_readl(&io, 0);
    mmio_unmap(&io);
    if (data != data2)
        return -1;
    else
       return 0;
}

void * mmiof_init(unsigned long iobase)
{
	struct 			mmio io1;
	unsigned long 	offset;
//	unsigned long 	iobase;
	unsigned long 	range;
	size_t			iosize;
	void			*iomem;
//	mmio_map(&io1, 0x18040000, 0);

	//memset(io1, 0, sizeof(*io1));

//	iobase = 0x18040000;
	//offset = 0;
	range  = 0;

//	mmio_normalize(&io1);
	int npages = 0;

	//iobase += offset;
	offset = iobase & (getpagesize() - 1);
	iobase = iobase & ~(getpagesize() - 1);

	npages += (range * sizeof(uint32_t)) / getpagesize();
	npages += 1;
	iosize = npages * getpagesize();

	//mmio_init(&io1);
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





// -----------------------------------------

/*
i2c_init(SCL_pin, SDA_pin, frequency=50)

i2c_start(addr | R/W-bit)
i2c_stop()

i2c_write(byte)
i2c_read(count)
*/











void * test_get_buffer(void)
{	
	return "1234567890";
}

void test_put_buffer(char * buffer)
{
	printf("C prints: %s\n", buffer);
}


