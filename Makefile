# Copyright (C) 2012 Žilvinas Valinskas, Saulius Lukšė
# See LICENSE for more information.

# PC Build single package
# cd /home/test/carambola2/
# clear; make package/pylibmmio-ath/clean
# clear; make package/pylibmmio-ath/compile V=99

# PC: http server
# cd /home/test/carambola2/bin/ar71xx/packages/; python -m SimpleHTTPServer

# PC: Carambola picocom
# sudo picocom -b 115200 /dev/ttyUSB0

# Carambola: get packet
# cd /tmp; rm pymmiolib*; wget http://192.168.0.63:8000/pymmiolib-ath_1_ar71xx.ipk; opkg install pymmiolib-ath_1_ar71xx.ipk


include $(TOPDIR)/rules.mk

PKG_NAME:=pymmiolib-ath
PKG_RELEASE:=1

PKG_BUILD_DIR := $(BUILD_DIR)/$(PKG_NAME)

include $(INCLUDE_DIR)/package.mk

define Package/$(PKG_NAME)
	SECTION:=utils
	CATEGORY:=Utilities
	TITLE:=Memory Mapped I/O library
endef

define Package/$(PKG_NAME)/description
	Memory Mapped I/O library
endef

define Build/Prepare
	mkdir -p $(PKG_BUILD_DIR)
	$(CP) ./src/* $(PKG_BUILD_DIR)/
endef

define Build/Compile
	make -C $(PKG_BUILD_DIR)		\
		$(TARGET_CONFIGURE_OPTS)	\
		CFLAGS="$(TARGET_CFLAGS) $(TARGET_CPPFLAGS)"	\
		LIBS="$(TARGET_LDFLAGS)"
endef

define Package/$(PKG_NAME)/install
	$(INSTALL_DIR) $(1)/usr/sbin
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/_libmmio.so $(1)/usr/sbin/_libmmio.so
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/libmmio.py $(1)/usr/sbin/libmmio.py
	
	# TODO: remove test program from package
	mkdir $(1)/test
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/test.py $(1)/test/test.py

endef

$(eval $(call BuildPackage,$(PKG_NAME)))
