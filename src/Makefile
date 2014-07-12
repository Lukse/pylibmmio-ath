libmmio:
	swig -python libmmio.i
	$(CC) -Wall -Os -fpic -c libmmio.c libmmio_wrap.c -I/usr/include/python2.7/
	#$(CC) -Wall -Os -fpic -c libmmio.c libmmio_wrap.c -I$(STAGING_DIR)/usr/include/python2.7/
	$(CC) -shared libmmio.o libmmio_wrap.o -o _libmmio.so

clean:
	rm *.o *.so hello libmmio_wrap.o
