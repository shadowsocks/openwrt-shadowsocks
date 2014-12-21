OpenWrt's ShadowSocks Makefile
===

 > 当前版本: 1.6.1-1  

功能说明
---

 > 可编译两种版本 

 - shadowsocks-libev

   > 官方原版  
   > 包含 `ss-{local,redir,tunnel}`  
   > 默认启动 ss-local 建立本地 SOCKS 代理  

 - shadowsocks-libev-spec

   > 针对 OpenWrt 的优化版本  
   > 包含 `ss-{redir,rules,tunnel}`  

   > `ss-redir` 建立透明代理  
   > `ss-rules` 生成代理规则  
   > `ss-tunnel` 提供 UDP 转发  
   > 从 `v1.5.2` 开始可以使用 [LuCI][L] 配置界面  

编译说明
---

 - 从 OpenWrt 的 [SDK][S] 编译, [预编译 IPK 下载][2]

 > ```bash
 > # 以 ar71xx 平台为例
 > tar xjf OpenWrt-SDK-ar71xx-for-linux-x86_64-gcc-4.8-linaro_uClibc-0.9.33.2.tar.bz2
 > cd OpenWrt-SDK-ar71xx-*
 > # 获取 Makefile
 > git clone https://github.com/aa65535/openwrt-shadowsocks.git package/shadowsocks-libev
 > # 选择要编译的包 Network -> shadowsocks-libev
 > make menuconfig
 > # 开始编译
 > make package/shadowsocks-libev/compile V=99
 > ```

配置说明
---

 - shadowsocks-libev 配置文件: `/etc/shadowsocks.json`

 - shadowsocks-libev-spec 配置文件: `/etc/shadowsocks/config.json`

 - [Ignore List][3]: `/etc/shadowsocks/ignore.list` 可以使用下面命令更新
    > ```bash
    > wget -O- 'http://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest' | awk -F\| '/CN\|ipv4/ { printf("%s/%d\n", $4, 32-log($5)/log(2)) }' > /etc/shadowsocks/ignore.list
    > ```

 - shadowsocks-libev-spec 从 `v1.5.2` 开始可以使用 [LuCI][L] 配置界面

相关项目
---

 Name                     | Description
 -------------------------|-----------------------------------
 [openwrt-chinadns][5]    | OpenWrt's ChinaDNS-C Makefile
 [openwrt-dnsmasq][6]     | OpenWrt's Dnsmasq Patch & Makefile
 [openwrt-shadowvpn][7]   | OpenWrt's ShadowVPN Makefile
 [openwrt-dist-luci][L]   | LuCI Applications of OpenWrt-dist


  [1]: https://github.com/madeye/shadowsocks-libev
  [2]: https://sourceforge.net/projects/openwrt-dist/files/shadowsocks-libev/
  [3]: https://github.com/aa65535/openwrt-shadowsocks/blob/master/files/shadowsocks.list
  [5]: https://github.com/aa65535/openwrt-chinadns
  [6]: https://github.com/aa65535/openwrt-dnsmasq
  [7]: https://github.com/aa65535/openwrt-shadowvpn
  [S]: http://downloads.openwrt.org/snapshots/trunk/
  [L]: https://github.com/aa65535/openwrt-dist-luci
