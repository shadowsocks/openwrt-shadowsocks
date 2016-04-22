Shadowsocks-libev for OpenWrt
===

简介
---

 本项目是 [shadowsocks-libev][1] 在 OpenWrt 上的移植  
 当前版本: [2.4.5-1][2]  

特性
---

可编译两种版本  

 - shadowsocks-libev

   ```
   原版/
   ├── etc/
   │   ├── init.d/
   │   │   └── shadowsocks   // init 脚本
   │   └── shadowsocks.json  // 配置文件
   └── usr/
       └── bin/
           ├── ss-local       // 提供 SOCKS 代理
           ├── ss-redir       // 提供透明代理, 从 v2.2.0 开始支持 UDP, 默认不启动
           └── ss-tunnel      // 提供 UDP 转发, 用于 DNS 查询, 默认不启动
   ```

 - shadowsocks-libev-spec

   ```
   优化版/
   ├── etc/
   │   ├── config/
   │   │   └── shadowsocks   // UCI 配置文件
   │   └── init.d/
   │       └── shadowsocks   // init 脚本
   └── usr/
       └── bin/
           ├── ss-redir       // 提供透明代理, 从 v2.2.0 开始支持 UDP
           ├── ss-rules       // 生成代理转发规则的脚本
           └── ss-tunnel      // 提供 UDP 转发, 用于 DNS 查询
   ```

编译
---

 - 从 OpenWrt 的 [SDK][S] 编译

   ```bash
   # 以 ar71xx 平台为例
   tar xjf OpenWrt-SDK-ar71xx-for-linux-x86_64-gcc-4.8-linaro_uClibc-0.9.33.2.tar.bz2
   cd OpenWrt-SDK-ar71xx-*
   # 获取 Makefile
   git clone https://github.com/shadowsocks/openwrt-shadowsocks.git package/shadowsocks-libev
   # 选择要编译的包 Network -> shadowsocks-libev
   make menuconfig
   # 开始编译
   make package/shadowsocks-libev/compile V=99
   ```

配置
---

 - shadowsocks-libev 配置文件: `/etc/shadowsocks.json`

 - shadowsocks-libev-spec 配置文件: `/etc/config/shadowsocks`

 - shadowsocks-libev-spec 从 `v1.5.2` 开始支持 [LuCI][L] 界面配置


  [1]: https://github.com/shadowsocks/shadowsocks-libev
  [2]: https://sourceforge.net/projects/openwrt-dist/files/shadowsocks-libev/ "预编译 IPK 下载"
  [L]: https://github.com/aa65535/openwrt-dist-luci "luci-app-shadowsocks-spec"
  [S]: https://wiki.openwrt.org/doc/howto/obtain.firmware.sdk
