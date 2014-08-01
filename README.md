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

 - [预编译 IPK 下载][2]

```
# 获取 Makefile
git clone https://github.com/aa65535/openwrt-shadowsocks.git package/network/shadowsocks
# 选择要编译的包 Network -> shadowsocks-libev
make menuconfig
# 开始编译 shadowsocks
rm -f dl/master.zip && make package/network/shadowsocks/compile V=99
# 若上面语句编译出错 使用下面语句编译
make V=99
```

配置说明
---

 - 默认使用透明代理模式启动 可编辑 `/etc/init.d/shadowsocks` 修改启动模式

```
start() {
    # Client Mode
    # service_start /usr/sbin/ss-local -c $CONFIG

    # Proxy Mode
    /usr/sbin/ss-rules -c $CONFIG -i $IGNORE && service_start /usr/sbin/ss-redir -c $CONFIG
}

stop() {
    # Client Mode
    # service_stop /usr/sbin/ss-local

    # Proxy Mode
    service_stop /usr/sbin/ss-redir && /etc/init.d/firewall restart>/dev/null 2>&1
}
```

 - ss-redir 配置文件: `/etc/shadowsocks/config.json`

```
{
    "server": "127.0.0.1",
    "server_port": 443,
    "local_port": 1080,
    "password": "password",
    "timeout": 60,
    "method": "aes-256-cfb"
}
```

 - ss-rules 配置文件: `/etc/shadowsocks/ignore.list`

```
# 可使用注释
; 0.0.0.0/7
# 14.0.0.0/8
- 14.0.12.0/22
# 生效部分
14.192.60.0
14.192.64.0/19
27.98.208.0/20
```

  [1]: https://github.com/madeye/shadowsocks-libev
  [2]: https://sourceforge.net/projects/openwrt-dist/files/shadowsocks-libev/
