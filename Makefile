#
# Copyright (C) 2014-2017 Jian Chang <aa65535@live.com>
#
# This is free software, licensed under the GNU General Public License v3.
# See /LICENSE for more information.
#

include $(TOPDIR)/rules.mk

PKG_NAME:=shadowsocks-libev
PKG_VERSION:=2.6.2
PKG_RELEASE:=1

PKG_SOURCE:=$(PKG_NAME)-$(PKG_VERSION).tar.gz
PKG_SOURCE_URL:=https://github.com/shadowsocks/openwrt-shadowsocks/releases/download/v$(PKG_VERSION)
PKG_MD5SUM:=6afee8b6ebcef21e8e921d198b93c362

PKG_LICENSE:=GPLv3
PKG_LICENSE_FILES:=LICENSE
PKG_MAINTAINER:=Max Lv <max.c.lv@gmail.com>

PKG_BUILD_DIR:=$(BUILD_DIR)/$(PKG_NAME)/$(BUILD_VARIANT)/$(PKG_NAME)-$(PKG_VERSION)

PKG_INSTALL:=1
PKG_FIXUP:=autoreconf
PKG_USE_MIPS16:=0
PKG_BUILD_PARALLEL:=1

include $(INCLUDE_DIR)/package.mk

define Package/shadowsocks-libev/Default
	SECTION:=net
	CATEGORY:=Network
	TITLE:=Lightweight Secured Socks5 Proxy $(2)
	URL:=https://github.com/shadowsocks/shadowsocks-libev
	VARIANT:=$(1)
	DEPENDS:=$(3) +libpcre +libpthread
endef

Package/shadowsocks-libev = $(call Package/shadowsocks-libev/Default,openssl,(OpenSSL),+libopenssl +zlib)
Package/shadowsocks-libev-server = $(Package/shadowsocks-libev)
Package/shadowsocks-libev-mbedtls = $(call Package/shadowsocks-libev/Default,mbedtls,(mbedTLS),+libmbedtls)
Package/shadowsocks-libev-server-mbedtls = $(Package/shadowsocks-libev-mbedtls)

define Package/shadowsocks-libev/description
Shadowsocks-libev is a lightweight secured socks5 proxy for embedded devices and low end boxes.
endef

Package/shadowsocks-libev-server/description = $(Package/shadowsocks-libev/description)
Package/shadowsocks-libev-mbedtls/description = $(Package/shadowsocks-libev/description)
Package/shadowsocks-libev-server-mbedtls/description = $(Package/shadowsocks-libev/description)

CONFIGURE_ARGS += --disable-ssp --disable-documentation --disable-assert

# Strip unused functions and data
TARGET_CFLAGS += -ffunction-sections -fdata-sections
TARGET_LDFLAGS += -Wl,--gc-sections

ifeq ($(BUILD_VARIANT),mbedtls)
	CONFIGURE_ARGS += --with-crypto-library=mbedtls
endif

define Package/shadowsocks-libev/install
	$(INSTALL_DIR) $(1)/usr/bin
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/src/ss-{local,redir,tunnel} $(1)/usr/bin
endef

Package/shadowsocks-libev-mbedtls/install = $(Package/shadowsocks-libev/install)

define Package/shadowsocks-libev-server/install
	$(INSTALL_DIR) $(1)/usr/bin
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/src/ss-server $(1)/usr/bin
endef

Package/shadowsocks-libev-server-mbedtls/install = $(Package/shadowsocks-libev-server/install)

$(eval $(call BuildPackage,shadowsocks-libev))
$(eval $(call BuildPackage,shadowsocks-libev-server))
$(eval $(call BuildPackage,shadowsocks-libev-mbedtls))
$(eval $(call BuildPackage,shadowsocks-libev-server-mbedtls))
