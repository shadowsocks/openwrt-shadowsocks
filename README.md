OpenWrt's ShadowSocks Makefile
===

 > 编译时默认从 [shadowsocks-libev][1] 下载最新源码

 > 保存文件名为 master.zip

 > 可使用如下方法强制每次编译时重新下载新的源码

 > 编辑 `scripts/download.pl` 相应部分改为:
 > ```perl
 > while (!$ok) {
 >     my $mirror = shift @mirrors;
 >     $mirror or die "No more mirrors to try - giving up.\n";
 >     $filename eq "master.zip" and unlink "$target/$filename";
 >     download($mirror);
 >     -f "$target/$filename" and $ok = 1;
 > }
 > 
 > ```

功能说明
---

 - 添加 `ss-rules` 可设置 `ignore.list` 中的 IP 不走代理

 - 移除不常用的 `ss-tunnel` 可安装附带的 `extra` 包添加

   > 安装后 `ss-tunnel` 默认会转发 `127.0.0.1:5353` 至 `8.8.4.4:53`

   > 相当于建立一个通过 `ShadowSocks` 服务器查询的本地 DNS 服务器

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
 > # 若上面语句编译出错 需要先使用下面语句编译出 Toolchain
 > make V=99
 > ```

配置说明
---

 - 默认使用透明代理模式启动 可编辑 `/etc/init.d/shadowsocks` 修改启动模式

 - ss-redir 配置文件: `/etc/shadowsocks/config.json`

 - ss-rules [配置文件][3]: `/etc/shadowsocks/ignore.list`
    > ```
    > # update command:
    > curl 'http://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest' | awk -F\| '/CN\|ipv4/ { printf("%s/%d\n", $4, 32-log($5)/log(2)) }' > /etc/shadowsocks/ignore.list
    > ```


  [1]: https://github.com/madeye/shadowsocks-libev
  [2]: https://sourceforge.net/projects/openwrt-dist/files/shadowsocks-libev/
  [3]: https://github.com/aa65535/openwrt-shadowsocks/blob/master/files/shadowsocks.list
