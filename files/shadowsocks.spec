#!/bin/sh /etc/rc.common

START=59

SERVICE_USE_PID=1
SERVICE_WRITE_PID=1
SERVICE_DAEMONIZE=1

CONFIG=/etc/shadowsocks/config.json
IGNORE=/etc/shadowsocks/ignore.list
SERVER=8.8.4.4:53

start() {
	/usr/bin/ss-rules -c $CONFIG -i $IGNORE && \
	service_start /usr/bin/ss-redir -c $CONFIG
	service_start /usr/bin/ss-tunnel -c $CONFIG -l 5353 -L $SERVER -u
}

stop() {
	service_stop /usr/bin/ss-tunnel
	service_stop /usr/bin/ss-redir && \
	/etc/init.d/firewall restart>/dev/null 2>&1
}
