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

start_rules() {
	local ac_ips
	local lan_ac_mode=$(uci_get_by_type access_control lan_ac_mode)
	local lan_ac_ips=$(uci_get_by_type access_control lan_ac_ips)
	server=$(uci_get_by_name $GLOBAL_SERVER server)
	local_port=$(uci_get_by_name $GLOBAL_SERVER local_port)
	if [ "$GLOBAL_SERVER" = "$UDP_RELAY_SERVER" ]; then
		ARG_UDP="-u"
	elif [ -n "$UDP_RELAY_SERVER" ]; then
		ARG_UDP="-U"
		udp_server=$(uci_get_by_name $UDP_RELAY_SERVER server)
		udp_local_port=$(uci_get_by_name $UDP_RELAY_SERVER local_port)
	fi
	if [ -n "$lan_ac_ips" ]; then
		case "$lan_ac_mode" in
			w|b) ac_ips="$lan_ac_mode$lan_ac_ips";;
		esac
	fi
	/usr/bin/ss-rules \
		-s "$server" \
		-l "$local_port" \
		-S "$udp_server" \
		-L "$udp_local_port" \
		-a "$ac_ips" \
		-i "$(uci_get_by_type access_control wan_bp_list)" \
		-b "$(uci_get_by_type access_control wan_bp_ips)" \
		-w "$(uci_get_by_type access_control wan_fw_ips)" \
		-e "$(uci_get_by_type access_control ipt_ext)" \
		-o $ARG_UDP
	return $?
}

start_redir() {
	case "$(uci_get_by_name $GLOBAL_SERVER auth_enable)" in
		1|on|true|yes|enabled) ARG_OTA="-A";;
	esac
	cat <<-EOF >$CONFIG_FILE
		{
		    "server": "$server",
		    "server_port": $(uci_get_by_name $GLOBAL_SERVER server_port),
		    "local_address": "0.0.0.0",
		    "local_port": $local_port,
		    "password": "$(uci_get_by_name $GLOBAL_SERVER password)",
		    "timeout": $(uci_get_by_name $GLOBAL_SERVER timeout 60),
		    "method": "$(uci_get_by_name $GLOBAL_SERVER encrypt_method)"
		}
EOF
	if [ "$ARG_UDP" = "-U" ]; then
		/usr/bin/ss-redir \
			-c $CONFIG_FILE $ARG_OTA \
			-f /var/run/ss-redir-tcp.pid
		case "$(uci_get_by_name $UDP_RELAY_SERVER auth_enable)" in
			1|on|true|yes|enabled) ARG_OTA="-A";;
			*) ARG_OTA="";;
		esac
		cat <<-EOF >$CONFIG_FILE
			{
			    "server": "$udp_server",
			    "server_port": $(uci_get_by_name $UDP_RELAY_SERVER server_port),
			    "local_address": "0.0.0.0",
			    "local_port": $udp_local_port,
			    "password": "$(uci_get_by_name $UDP_RELAY_SERVER password)",
			    "timeout": $(uci_get_by_name $UDP_RELAY_SERVER timeout 60),
			    "method": "$(uci_get_by_name $UDP_RELAY_SERVER encrypt_method)"
			}
EOF
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

boot() {
	until iptables-save -t nat | grep -q "^:zone_lan_prerouting"; do
		sleep 1
	done
	start
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

stop() {
	/usr/bin/ss-rules -f
	killall -q -9 ss-redir
	killall -q -9 ss-tunnel
}
