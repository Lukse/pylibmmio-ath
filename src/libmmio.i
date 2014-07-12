%module libmmio
%include "cdata.i"

%{

#include <stdbool.h>

%}

# TODO: use these defines only in one place, looks like these defines are used only in swig wrapper

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

%{
unsigned long mmio_read(unsigned long iobase);
unsigned long mmio_write(unsigned long iobase, unsigned long data2);
void * mmiof_init(unsigned long iobase);
unsigned long mmiof_read(void * iomem, unsigned long offset);
void mmiof_write(void * iomem, unsigned long offset, unsigned long value);
void mmiof_close(void * iomem); 

void * test_get_buffer(void);
void test_put_buffer(char * buffer);

void pin_set(void * iomem, unsigned int bit);
void pin_clear(void * iomem, unsigned int bit);
unsigned int pin_read(void * iomem, unsigned int bit);
void pin_direction(void * iomem, unsigned int bit, unsigned int direction);
%}

unsigned long mmio_read(unsigned long iobase);
unsigned long mmio_write(unsigned long iobase, unsigned long data2);
void * mmiof_init(unsigned long iobase);
unsigned long mmiof_read(void * iomem, unsigned long offset);
void mmiof_write(void * iomem, unsigned long offset, unsigned long value);
void mmiof_close(void * iomem); 

void * test_get_buffer(void);
void test_put_buffer(char * buffer);

void pin_set(void * iomem, unsigned int bit);
void pin_clear(void * iomem, unsigned int bit);
unsigned int pin_read(void * iomem, unsigned int bit);
void pin_direction(void * iomem, unsigned int bit, unsigned int direction);
