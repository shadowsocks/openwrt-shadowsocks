Shadowsocks-libev-full for OpenWrt   
===

简介
---

 本项目是 [shadowsocks-libev][1] 在 OpenWrt 上的完整移植，包括服务器端和客户端。   
 当前版本: 2.4.5-1  
 [预编译 ipk 下载][R]

特性
---

可编译 两种客户端版本 和 一种服务器端版本

 - shadowsocks-libev

   > 官方原版
   > 可执行文件 `ss-{local,redir,tunnel}`  
   > 默认启动:  
   > `ss-redir` 提供透明代理  
   > `ss-tunnel` 提供 UDP 转发, 用于 DNS 查询  

 - shadowsocks-libev-spec

   > 针对 OpenWrt 的优化版本
   > 可执行文件 `ss-{redir,rules,tunnel}`  
   > 默认启动:  
   > `ss-redir` 提供透明代理  
   > `ss-rules` 生成代理转发规则  
   > `ss-tunnel` 提供 UDP 转发, 用于 DNS 查询  

 - shadowsocks-libev-server

   > 官方原版服务器端
   > 可执行文件 `ss-server`  
   > 默认启动:  
   > `ss-server` 提供 shadowsocks 服务  

编译
---

 - 从 OpenWrt 的 [SDK][S] 编译

   ```bash
   # 以 OpenWrt Chaos Calmer 15.05 ar71xx 平台为例
   wget https://downloads.openwrt.org/chaos_calmer/15.05/ar71xx/generic/OpenWrt-SDK-15.05-ar71xx-generic_gcc-4.8-linaro_uClibc-0.9.33.2.Linux-x86_64.tar.bz2
   tar xjf OpenWrt-SDK-15.05-ar71xx-generic_gcc-4.8-linaro_uClibc-0.9.33.2.Linux-x86_64.tar.bz2
   cd OpenWrt-SDK-15.05-ar71xx-*
   # 获取 Makefile
   git clone https://github.com/bettermanbao/openwrt-shadowsocks-libev-full.git package/shadowsocks-libev-full
   # 选择要编译的包 Network -> shadowsocks-libev
   make menuconfig
   # 开始编译
   make package/shadowsocks-libev-full/compile V=s
   ```

配置
---

 - shadowsocks-libev 配置文件: `/etc/shadowsocks.json`

 - shadowsocks-libev-spec 配置文件: `/etc/config/shadowsocks`

 - shadowsocks-libev-spec 从 `v1.5.2` 开始可以使用 [LuCI][L] 配置界面

 - shadowsocks-libev-server 配置文件: `/etc/config/shadowsocks-server.json`

----------


  [1]: https://github.com/shadowsocks/shadowsocks-libev
  [R]: https://github.com/bettermanbao/openwrt-shadowsocks-libev-full/releases
  [L]: https://github.com/aa65535/openwrt-dist-luci
  [S]: http://wiki.openwrt.org/doc/howto/obtain.firmware.sdk
