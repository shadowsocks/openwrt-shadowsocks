include $(TOPDIR)/rules.mk

PKG_NAME:=shadowsocks-libev
PKG_VERSION:=1.4.8
PKG_RELEASE=3

PKG_SOURCE:=master.zip
PKG_SOURCE_URL:=https://github.com/madeye/shadowsocks-libev/archive
PKG_CAT:=unzip
PKG_MAINTAINER:=Max Lv <max.c.lv@gmail.com>

PKG_BUILD_DIR:=$(BUILD_DIR)/$(PKG_NAME)/$(BUILD_VARIANT)/$(PKG_NAME)-master

PKG_INSTALL:=1
PKG_FIXUP:=autoreconf
PKG_USE_MIPS16:=0
PKG_BUILD_PARALLEL:=1

include $(INCLUDE_DIR)/package.mk

define Package/shadowsocks-libev/Default
	SECTION:=net
	CATEGORY:=Network
	TITLE:=Lightweight Secured Socks5 Proxy $(2)
	URL:=https://github.com/madeye/shadowsocks-libev
	VARIANT:=$(1)
	DEPENDS:=$(3)
endef

Package/shadowsocks-libev = $(call Package/shadowsocks-libev/Default,openssl,(OpenSSL),+libopenssl)
Package/shadowsocks-libev-spec = $(call Package/shadowsocks-libev/Default,openssl,(OpenSSL),+libopenssl)
Package/shadowsocks-libev-polarssl = $(call Package/shadowsocks-libev/Default,polarssl,(PolarSSL),+libpolarssl)
Package/shadowsocks-libev-spec-polarssl = $(call Package/shadowsocks-libev/Default,polarssl,(PolarSSL),+libpolarssl)

define Package/shadowsocks-libev/description
Shadowsocks-libev is a lightweight secured scoks5 proxy for embedded devices and low end boxes.
endef

Package/shadowsocks-libev-spec/description = $(Package/shadowsocks-libev/description)
Package/shadowsocks-libev-polarssl/description = $(Package/shadowsocks-libev/description)
Package/shadowsocks-libev-spec-polarssl/description = $(Package/shadowsocks-libev/description)

define Package/shadowsocks-libev/conffiles
/etc/shadowsocks.json
endef

define Package/shadowsocks-libev-spec/conffiles
/etc/shadowsocks/config.json
/etc/shadowsocks/ignore.list
endef

Package/shadowsocks-libev-polarssl/conffiles = $(Package/shadowsocks-libev/conffiles)
Package/shadowsocks-libev-spec-polarssl/conffiles = $(Package/shadowsocks-libev-spec/conffiles)

ifeq ($(BUILD_VARIANT),polarssl)
	CONFIGURE_ARGS += --with-crypto-library=polarssl
endif

define Package/shadowsocks-libev/install
	$(INSTALL_DIR) $(1)/usr/bin
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/src/ss-{local,redir,tunnel} $(1)/usr/bin
	$(INSTALL_DIR) $(1)/etc/init.d
	$(INSTALL_CONF) ./files/shadowsocks.conf $(1)/etc/shadowsocks.json
	$(INSTALL_BIN) ./files/shadowsocks.init $(1)/etc/init.d/shadowsocks
endef

define Package/shadowsocks-libev-spec/install
	$(INSTALL_DIR) $(1)/usr/bin
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/src/ss-{redir,tunnel} $(1)/usr/bin
	$(INSTALL_BIN) ./files/shadowsocks.rule $(1)/usr/bin/ss-rules
	$(INSTALL_DIR) $(1)/etc/shadowsocks
	$(INSTALL_CONF) ./files/shadowsocks.conf $(1)/etc/shadowsocks/config.json
	$(INSTALL_CONF) ./files/shadowsocks.list $(1)/etc/shadowsocks/ignore.list
	$(INSTALL_DIR) $(1)/etc/init.d
	$(INSTALL_BIN) ./files/shadowsocks.spec $(1)/etc/init.d/shadowsocks
	$(INSTALL_DIR) $(1)/etc/hotplug.d/iface
	$(INSTALL_DATA) ./files/shadowsocks.hotplug $(1)/etc/hotplug.d/iface/30-shadowsocks
endef

Package/shadowsocks-libev-polarssl/install = $(Package/shadowsocks-libev/install)
Package/shadowsocks-libev-spec-polarssl/install = $(Package/shadowsocks-libev-spec/install)

$(shell $(RM) $(DL_DIR)/$(PKG_SOURCE))
$(eval $(call BuildPackage,shadowsocks-libev))
$(eval $(call BuildPackage,shadowsocks-libev-spec))
$(eval $(call BuildPackage,shadowsocks-libev-polarssl))
$(eval $(call BuildPackage,shadowsocks-libev-spec-polarssl))
