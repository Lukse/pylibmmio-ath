%module libmmio

%{
unsigned long mmio_read(unsigned long iobase);
unsigned long mmio_write(unsigned long iobase, unsigned long data2);
void * mmiof_init(unsigned long iobase);
unsigned long mmiof_read(void * iomem, unsigned long offset);
void mmiof_write(void * iomem, unsigned long offset, unsigned long value);
void mmiof_close(void * iomem); 
%}

unsigned long mmio_read(unsigned long iobase);
unsigned long mmio_write(unsigned long iobase, unsigned long data2);
void * mmiof_init(unsigned long iobase);
unsigned long mmiof_read(void * iomem, unsigned long offset);
void mmiof_write(void * iomem, unsigned long offset, unsigned long value);
void mmiof_close(void * iomem); 
