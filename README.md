OpenWrt's ShadowSocks Makefile
===

 > 编译时默认从 [madeye/shadowsocks-libev][1] 下载最新源码

功能说明
---

 > 可编译两种版本  

 - shadowsocks-libev  

   > 官方原版  
   > 包含 `ss-{local,redir,tunnel}` 三个可执行文件  
   > 默认启动 ss-local 建立本地 SOCKS 代理  

 - shadowsocks-libev-spec

   > 针对 OpenWrt 路由器的优化版本  
   > 包含 `ss-{redir,rules,tunnel}` 三个可执行文件  
   > `ss-redir` 建立透明代理, `ss-tunnel` 做 DNS 查询转发  

   > `ss-tunnel` 默认转发 `127.0.0.1:5353` 至 `8.8.4.4:53`  
   > 通过 `ShadowSocks` 服务器查询 DNS 用于线路优化  

   > `ss-rules` 可设置 `ignore.list` 中的 IP 流量不走代理  
   > `ss-rules` 可支持 `ipset` 和 `iptables` 两种转发规则  
   > 默认使用性能更好的 `ipset` 规则, 对不支持的设备使用 `iptables`  

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
    > curl 'http://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest' | awk -F\| '/CN\|ipv4/ { printf("%s/%d\n", $4, 32-log($5)/log(2)) }' > /etc/shadowsocks/ignore.list
    > ```

相关项目
---

 Name                     | Description
 -------------------------|-----------------------------------
 [openwrt-chinadns][5]    | OpenWrt's ChinaDNS-C Makefile
 [openwrt-dnsmasq][6]     | OpenWrt's Dnsmasq Patch & Makefile
 [openwrt-shadowvpn][7]   | OpenWrt's ShadowVPN Makefile


  [1]: https://github.com/madeye/shadowsocks-libev
  [2]: https://sourceforge.net/projects/openwrt-dist/files/shadowsocks-libev/
  [3]: https://github.com/aa65535/openwrt-shadowsocks/blob/master/files/shadowsocks.list
  [5]: https://github.com/aa65535/openwrt-chinadns
  [6]: https://github.com/aa65535/openwrt-dnsmasq
  [7]: https://github.com/aa65535/openwrt-shadowvpn
  [S]: http://downloads.openwrt.org/snapshots/trunk/
