#!/bin/sh /etc/rc.common
#
# Copyright (C) 2016 OpenWrt-dist
# Copyright (C) 2016 Jian Chang <aa65535@live.com>
#
# This is free software, licensed under the GNU General Public License v3.
# See /LICENSE for more information.
#

START=90
STOP=15

NAME=shadowsocks
EXTRA_COMMANDS=rules
GLOBAL_CONFIG_FILE=/var/etc/$NAME.json
UDP_RELAY_CONFIG_FILE=/var/etc/$NAME-udp.json

uci_get_by_name() {
	local ret=$(uci get $NAME.$1.$2 2>/dev/null)
	echo ${ret:=$3}
}

uci_get_by_type() {
	local ret=$(uci get $NAME.@$1[0].$2 2>/dev/null)
	echo ${ret:=$3}
}

get_arg_ota() {
	case "$(uci_get_by_name $1 auth)" in
		1|on|true|yes|enabled) echo "-A";;
	esac
}

gen_config_file() {
	cat <<-EOF >$2
		{
		    "server": "$(uci_get_by_name $1 server)",
		    "server_port": $(uci_get_by_name $1 server_port),
		    "local_address": "0.0.0.0",
		    "local_port": $(uci_get_by_name $1 local_port),
		    "password": "$(uci_get_by_name $1 password)",
		    "timeout": $(uci_get_by_name $1 timeout 60),
		    "method": "$(uci_get_by_name $1 encrypt_method)"
		}
EOF
}

gen_lan_hosts() {
	case "$(uci_get_by_name $1 enable)" in
		1|on|true|yes|enabled)
			echo "$(uci_get_by_name $1 type),$(uci_get_by_name $1 host)";;
	esac
}

start_rules() {
	local server=$(uci_get_by_name $GLOBAL_SERVER server)
	local local_port=$(uci_get_by_name $GLOBAL_SERVER local_port)
	if [ "$GLOBAL_SERVER" = "$UDP_RELAY_SERVER" ]; then
		ARG_UDP="-u"
	elif [ -n "$UDP_RELAY_SERVER" ]; then
		ARG_UDP="-U"
		local udp_server=$(uci_get_by_name $UDP_RELAY_SERVER server)
		local udp_local_port=$(uci_get_by_name $UDP_RELAY_SERVER local_port)
	fi
	config_load $NAME
	/usr/bin/ss-rules \
		-s "$server" \
		-l "$local_port" \
		-S "$udp_server" \
		-L "$udp_local_port" \
		-i "$(uci_get_by_type access_control wan_bp_list)" \
		-b "$(uci_get_by_type access_control wan_bp_ips)" \
		-w "$(uci_get_by_type access_control wan_fw_ips)" \
		-I "$(uci_get_by_type access_control lan_ifaces br-lan)" \
		-d "$(uci_get_by_type access_control lan_target)" \
		-a "$(echo $(config_foreach gen_lan_hosts lan_hosts))" \
		-e "$(uci_get_by_type access_control ipt_ext)" \
		-o $ARG_UDP
		local ret=$?
		[ "$ret" = 0 ] || /usr/bin/ss-rules -f
	return $ret
}

rules() {
	GLOBAL_SERVER=$(uci_get_by_type global global_server)
	[ "$GLOBAL_SERVER" = "nil" ] && exit 0
	mkdir -p /var/run /var/etc
	UDP_RELAY_SERVER=$(uci_get_by_type global udp_relay_server)
	[ "$UDP_RELAY_SERVER" = "same" ] && UDP_RELAY_SERVER=$GLOBAL_SERVER
	start_rules
}

start_redir() {
	gen_config_file $1 $2
	/usr/bin/ss-redir -c $2 $3 $(get_arg_ota $1) -f /var/run/ss-redir$4.pid
}

redir() {
	case "$ARG_UDP" in
		-u)
			start_redir $GLOBAL_SERVER $GLOBAL_CONFIG_FILE -u
			;;
		-U)
			start_redir $GLOBAL_SERVER $GLOBAL_CONFIG_FILE
			start_redir $UDP_RELAY_SERVER $UDP_RELAY_CONFIG_FILE -U -udp
			;;
		*)
			start_redir $GLOBAL_SERVER $GLOBAL_CONFIG_FILE
			;;
	esac
}

start_tunnel() {
	/usr/bin/ss-tunnel -c $2 $3 $(get_arg_ota $1) \
		-l $(uci_get_by_type port_forward local_port 5300) \
		-L $(uci_get_by_type port_forward destination 8.8.4.4:53) \
		-f /var/run/ss-tunnel$4.pid
}

tunnel() {
	case "$ARG_UDP" in
		-U)
			start_tunnel $GLOBAL_SERVER $GLOBAL_CONFIG_FILE
			start_tunnel $UDP_RELAY_SERVER $UDP_RELAY_CONFIG_FILE -U -udp
			;;
		*)
			start_tunnel $GLOBAL_SERVER $GLOBAL_CONFIG_FILE -u
			;;
	esac
}

start() {
	rules && redir
	case "$(uci_get_by_type port_forward enable)" in
		1|on|true|yes|enabled) tunnel;;
	esac
}

kill_pid() {
	local pid=$(cat $1 2>/dev/null)
	rm -f $1
	if [ -n "$pid" -a -d "/proc/$pid" ]; then
		kill -9 $pid
	fi
}

stop() {
	/usr/bin/ss-rules -f
	kill_pid /var/run/ss-redir.pid
	kill_pid /var/run/ss-redir-udp.pid
	kill_pid /var/run/ss-tunnel.pid
	kill_pid /var/run/ss-tunnel-udp.pid
}
