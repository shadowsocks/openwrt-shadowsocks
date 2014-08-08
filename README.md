OpenWrt's ShadowSocks Makefile
===

 > 编译时默认从 [shadowsocks-libev][1] 下载最新源码

功能说明
---

 - 添加 `ss-rules` 可设置 `ignore.list` 中的 IP 不走代理

 - 移除不常用的 `ss-tunnel` 可安装附带的 `extra` 包添加

 - 修改安装位置为 `/usr/sbin` 需先卸载已安装的其他版本

编译说明
---

 - OpenWrt 平台的编译, [预编译 IPK 下载][2]

 > ```
 > # 获取 Makefile
 > git clone https://github.com/aa65535/openwrt-shadowsocks.git package/network/shadowsocks
 > # 选择要编译的包 Network -> shadowsocks-libev
 > make menuconfig
 > # 开始编译 shadowsocks
 > rm -f dl/master.zip && make package/network/shadowsocks/compile V=99
 > # 若上面语句编译出错 使用下面语句编译
 > make V=99
 > ```

配置说明
---

 - 默认使用透明代理模式启动 可编辑 `/etc/init.d/shadowsocks` 修改启动模式

 - ss-redir 配置文件: `/etc/shadowsocks/config.json`

 - ss-rules 配置文件: `/etc/shadowsocks/ignore.list`


  [1]: https://github.com/madeye/shadowsocks-libev
  [2]: https://sourceforge.net/projects/openwrt-dist/files/shadowsocks-libev/
