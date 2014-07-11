shadowsocks 的 OpenWrt Makefile
===

默认从 [shadowsocks-libev][1] 下载最新源码进行编译

使用说明
---

```
# 下载 Makefile
git clone https://github.com/aa65535/openwrt-shadowsocks.git package/network/services/shadowsocks
# 选择要编译的包
make menuconfig
# 开始编译
rm dl/master.zip
make package/network/services/shadowsocks/compile V=99
```

默认使用透明代理模式启动
通过修改`/etc/init.d/shadowsocks`调整启动模式


  [1]: https://github.com/madeye/shadowsocks-libev
