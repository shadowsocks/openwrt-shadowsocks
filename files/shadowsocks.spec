#!/bin/sh /etc/rc.common
#
# Copyright (C) 2015 OpenWrt-dist
# Copyright (C) 2015 Jian Chang <aa65535@live.com>
#
# This is free software, licensed under the GNU General Public License v3.
# See /LICENSE for more information.
#

START=90
STOP=15

NAME=shadowsocks
EXTRA_COMMANDS=rules
CONFIG_FILE=/var/etc/$NAME.json

uci_get_by_name() {
	local ret=$(uci get $NAME.$1.$2 2>/dev/null)
	echo ${ret:=$3}
}

uci_get_by_type() {
	local ret=$(uci get $NAME.@$1[0].$2 2>/dev/null)
	echo ${ret:=$3}
}

gen_config_file() {
	cat <<-EOF >$CONFIG_FILE
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
	/usr/bin/ss-rules \
		-s "$server" \
		-l "$local_port" \
		-S "$udp_server" \
		-L "$udp_local_port" \
		-i "$(uci_get_by_type access_control wan_bp_list)" \
		-b "$(uci_get_by_type access_control wan_bp_ips)" \
		-w "$(uci_get_by_type access_control wan_fw_ips)" \
		-d "$(uci_get_by_type access_control lan_default_target)" \
		-I "$(uci_get_by_type access_control interface lan)" \
		-a "$(uci_get_by_type access_control lan_hosts_action)" \
		-e "$(uci_get_by_type access_control ipt_ext)" \
		-o $ARG_UDP
		local ret=$?
		[ "$ret" = 0 ] || /usr/bin/ss-rules -f
	return $ret
}

start_redir() {
	case "$(uci_get_by_name $GLOBAL_SERVER auth_enable)" in
		1|on|true|yes|enabled) ARG_OTA="-A";;
		*) ARG_OTA="";;
	esac
	gen_config_file $GLOBAL_SERVER
	if [ "$ARG_UDP" = "-U" ]; then
		/usr/bin/ss-redir \
			-c $CONFIG_FILE $ARG_OTA \
			-f /var/run/ss-redir-tcp.pid
		case "$(uci_get_by_name $UDP_RELAY_SERVER auth_enable)" in
			1|on|true|yes|enabled) ARG_OTA="-A";;
			*) ARG_OTA="";;
		esac
		gen_config_file $UDP_RELAY_SERVER
	fi
	/usr/bin/ss-redir \
		-c $CONFIG_FILE $ARG_OTA $ARG_UDP \
		-f /var/run/ss-redir.pid
	return $?
}

start_tunnel() {
	/usr/bin/ss-tunnel \
		-c $CONFIG_FILE $ARG_OTA ${ARG_UDP:="-u"} \
		-l $(uci_get_by_type udp_forward tunnel_port 5300) \
		-L $(uci_get_by_type udp_forward tunnel_forward 8.8.4.4:53) \
		-f /var/run/ss-tunnel.pid
	return $?
}

rules() {
	GLOBAL_SERVER=$(uci_get_by_type global global_server)
	[ "$GLOBAL_SERVER" = "nil" ] && exit 0
	mkdir -p /var/run /var/etc
	UDP_RELAY_SERVER=$(uci_get_by_type global udp_relay_server)
	[ "$UDP_RELAY_SERVER" = "same" ] && UDP_RELAY_SERVER=$GLOBAL_SERVER
	start_rules
}

start() {
	rules && start_redir
	case "$(uci_get_by_type udp_forward tunnel_enable)" in
		1|on|true|yes|enabled) start_tunnel;;
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
	kill_pid /var/run/ss-redir-tcp.pid
	kill_pid /var/run/ss-tunnel.pid
}
