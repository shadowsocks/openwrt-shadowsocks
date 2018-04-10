#
# Copyright (C) 2014-2017 Jian Chang <aa65535@live.com>
#
# This is free software, licensed under the GNU General Public License v3.
# See /LICENSE for more information.
#

include $(TOPDIR)/rules.mk

PKG_NAME:=shadowsocks-libev
PKG_VERSION:=3.1.3
PKG_RELEASE:=4

PKG_SOURCE_PROTO:=git
PKG_SOURCE_URL:=https://github.com/shadowsocks/shadowsocks-libev.git
PKG_SOURCE_VERSION:=a9d56518bb3e0662e76f60e0ce087a35d6af8323
PKG_SOURCE_SUBDIR:=$(PKG_NAME)-$(PKG_VERSION)-$(PKG_SOURCE_VERSION)
PKG_SOURCE:=$(PKG_NAME)-$(PKG_VERSION)-$(PKG_SOURCE_VERSION).tar.xz

PKG_LICENSE:=GPLv3
PKG_LICENSE_FILES:=LICENSE
PKG_MAINTAINER:=Jian Chang <aa65535@live.com>

PKG_BUILD_DIR:=$(BUILD_DIR)/$(PKG_NAME)/$(BUILD_VARIANT)/$(PKG_NAME)-$(PKG_VERSION)-$(PKG_SOURCE_VERSION)

PKG_INSTALL:=1
PKG_FIXUP:=autoreconf
PKG_USE_MIPS16:=0
PKG_BUILD_PARALLEL:=1

include $(INCLUDE_DIR)/package.mk

define Package/shadowsocks-libev/Default
	SECTION:=net
	CATEGORY:=Network
	TITLE:=Lightweight Secured Socks5 Proxy
	URL:=https://github.com/shadowsocks/shadowsocks-libev
	VARIANT:=$(1)
	DEPENDS:=$(2)
endef

Package/shadowsocks-libev = $(call Package/shadowsocks-libev/Default,shared,+zlib +libpthread +libev +libcares +libpcre +libsodium +libmbedtls)
Package/shadowsocks-libev-server = $(call Package/shadowsocks-libev/Default,shared,+zlib +libpthread +libev +libcares +libpcre +libsodium +libmbedtls)

Package/shadowsocks-libev-static = $(call Package/shadowsocks-libev/Default,static,+zlib +libpthread)
Package/shadowsocks-libev-server-static = $(call Package/shadowsocks-libev/Default,static,+zlib +libpthread)

define Package/shadowsocks-libev/description
Shadowsocks-libev is a lightweight secured socks5 proxy for embedded devices and low end boxes.
endef

Package/shadowsocks-libev-server/description = $(Package/shadowsocks-libev/description)

Package/shadowsocks-libev-static/description = $(Package/shadowsocks-libev/description)
Package/shadowsocks-libev-server-static/description = $(Package/shadowsocks-libev/description)

CONFIGURE_ARGS += \
				--disable-ssp \
				--disable-documentation \
				--disable-assert

ifeq ($(BUILD_VARIANT),static)
	CONFIGURE_ARGS += \
				--with-ev="$(STAGING_DIR)/usr" \
				--with-pcre="$(STAGING_DIR)/usr" \
				--with-cares="$(STAGING_DIR)/usr" \
				--with-mbedtls="$(STAGING_DIR)/usr" \
				--with-sodium="$(STAGING_DIR)/usr" \
				LDFLAGS="-Wl,-static -static -static-libgcc"
endif

define Package/shadowsocks-libev/install
	$(INSTALL_DIR) $(1)/usr/bin
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/src/ss-{local,redir,tunnel} $(1)/usr/bin
endef

Package/shadowsocks-libev-static/install = $(Package/shadowsocks-libev/install)

define Package/shadowsocks-libev-server/install
	$(INSTALL_DIR) $(1)/usr/bin
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/src/ss-server $(1)/usr/bin
endef

Package/shadowsocks-libev-server-static/install = $(Package/shadowsocks-libev-server/install)

$(eval $(call BuildPackage,shadowsocks-libev))
$(eval $(call BuildPackage,shadowsocks-libev-server))

$(eval $(call BuildPackage,shadowsocks-libev-static))
$(eval $(call BuildPackage,shadowsocks-libev-server-static))
