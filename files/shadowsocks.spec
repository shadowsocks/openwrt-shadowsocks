#!/bin/sh /etc/rc.common

START=99

SERVICE_USE_PID=1
SERVICE_WRITE_PID=1
SERVICE_DAEMONIZE=1

CONFIG=/etc/shadowsocks/config.json
IGNORE=/etc/shadowsocks/ignore.list
EXT_ARGS=""

start() {
	/usr/bin/ss-rules -c $CONFIG -i $IGNORE -e "$EXT_ARGS" && \
	service_start /usr/bin/ss-redir -c $CONFIG
	service_start /usr/bin/ss-tunnel -c $CONFIG -t 10 -l 5353 -L 8.8.4.4:53 -u
}

stop() {
	/usr/bin/ss-rules -c $CONFIG -e "$EXT_ARGS" -f && \
	service_stop /usr/bin/ss-redir
	service_stop /usr/bin/ss-tunnel
}

reload() {
	/usr/bin/ss-rules -c $CONFIG -i $IGNORE -e "$EXT_ARGS"
}
