#!/bin/sh /etc/rc.common

START=90
STOP=15

SERVICE_USE_PID=1
SERVICE_WRITE_PID=1
SERVICE_DAEMONIZE=1
EXTRA_COMMANDS="rules"

get_args() {
	config_get_bool enable $1 enable
	config_get_bool use_conf_file $1 use_conf_file
	config_get config_file $1 config_file
	config_get server $1 server
	config_get server_port $1 server_port
	config_get local_port $1 local_port
	config_get password $1 password
	config_get encrypt_method $1 encrypt_method
	config_get ignore_list $1 ignore_list
	config_get_bool tunnel_enable $1 tunnel_enable
	config_get tunnel_port $1 tunnel_port
	config_get tunnel_forward $1 tunnel_forward
	config_get lan_ac_mode $1 lan_ac_mode
	config_get lan_ac_ip $1 lan_ac_ip
	: ${local_port:=1080}
	: ${tunnel_port:=5353}
	: ${tunnel_forward:=8.8.4.4:53}
	: ${config_file:=/etc/shadowsocks/config.json}
}

check_args() {
	local ERR="not defined"
	while [ -n "$1" ]; do
		case $1 in
			s)
				: ${server:?$ERR}
				;;
			p)
				: ${server_port:?$ERR}
				;;
			k)
				: ${password:?$ERR}
				;;
			m)
				: ${encrypt_method:?$ERR}
				;;
		esac
		shift
	done
	return 0
}

start_rules() {
	local ac_args

	if [ -n "$lan_ac_ip" ]; then
		case $lan_ac_mode in
			1) ac_args="w$lan_ac_ip"
			;;
			2) ac_args="b$lan_ac_ip"
			;;
		esac
	fi

	if [ "$use_conf_file" = 1 ]; then
		/usr/bin/ss-rules \
			-c "$config_file" \
			-i "$ignore_list" \
			-a "$ac_args"
	else
		check_args s
		/usr/bin/ss-rules \
			-s "$server" \
			-l "$local_port" \
			-i "$ignore_list" \
			-a "$ac_args"
	fi
	return $?
}

start_redir() {
	if [ "$use_conf_file" = 1 ]; then
		service_start /usr/bin/ss-redir \
			-c "$config_file"
	else
		check_args s p k m
		service_start /usr/bin/ss-redir \
			-s "$server" \
			-p "$server_port" \
			-l "$local_port" \
			-k "$password" \
			-m "$encrypt_method"
	fi
	return $?
}

start_tunnel() {
	if [ "$use_conf_file" = 1 ]; then
		service_start /usr/bin/ss-tunnel \
			-c "$config_file" \
			-l "$tunnel_port" \
			-L "$tunnel_forward" \
			-u
	else
		check_args s p k m
		service_start /usr/bin/ss-tunnel \
			-s "$server" \
			-p "$server_port" \
			-k "$password" \
			-m "$encrypt_method" \
			-l "$tunnel_port" \
			-L "$tunnel_forward" \
			-u
	fi
	return $?
}

rules() {
	config_load shadowsocks
	config_foreach get_args shadowsocks
	[ "$enable" = 1 ] || exit 0
	start_rules
}

start() {
	rules && start_redir
	[ "$tunnel_enable" = 1 ] && start_tunnel
}

boot() {
	until iptables-save -t nat | grep -q "^-A zone_lan_prerouting"; do
		sleep 1
	done
	start
}

stop() {
	/usr/bin/ss-rules -f
	service_stop /usr/bin/ss-redir
	service_stop /usr/bin/ss-tunnel
}
