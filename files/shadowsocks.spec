#!/bin/sh /etc/rc.common

START=95

SERVICE_USE_PID=1
SERVICE_WRITE_PID=1
SERVICE_DAEMONIZE=1
EXTRA_COMMANDS="rules"

append_arg() {
	local cfg="$1"
	local var="$2"
	local opt="$3"
	local val
	config_get val "$cfg" "$var"
	[ -n "$val" ] && args="$args $opt \"$val\""
}

start_rules() {
	local enable ac_mode source_ip use_conf_file
	config_get_bool enable $1 enable
	[ "$enable" = 1 ] || return 0
	args=""
	config_get_bool use_conf_file $1 use_conf_file
	if [ "$use_conf_file" = 1 ]; then
		append_arg $1 config_file "-c"
	else
		append_arg $1 server "-s"
		append_arg $1 local_port "-l"
	fi
	[ -z "$args" ] && return 2
	append_arg $1 ignore_list "-i"
	config_get ac_mode $1 ac_mode
	if [ "$ac_mode" = 1 ]; then
		config_get source_ip $1 accept_ip
		source_ip=$(echo $source_ip | tr ' ' ',')
		[ -n "$source_ip" ] && args="$args -e \"-s $source_ip\""
	fi
	if [ "$ac_mode" = 2 ]; then
		config_get source_ip $1 reject_ip
		[ -n "$source_ip" ] && args="$args -e \"! -s $source_ip\""
	fi
	eval "/usr/bin/ss-rules $args"
	return $?
}

start_redir() {
	local enable use_conf_file
	config_get_bool enable $1 enable
	[ "$enable" = 1 ] || return 0
	args=""
	config_get_bool use_conf_file $1 use_conf_file
	if [ "$use_conf_file" = 1 ]; then
		append_arg $1 config_file "-c"
	else
		append_arg $1 server "-s"
		append_arg $1 server_port "-p"
		append_arg $1 local_port "-l"
		append_arg $1 password "-k"
		append_arg $1 encrypt_method "-m"
	fi
	[ -z "$args" ] && return 2
	eval "service_start /usr/bin/ss-redir $args"
	return $?
}

start_tunnel() {
	local enable tunnel_enable use_conf_file
	config_get_bool enable $1 enable
	config_get_bool tunnel_enable $1 tunnel_enable
	[ "$enable" = 1 -a "$tunnel_enable" = 1 ] || return 0
	args=""
	config_get_bool use_conf_file $1 use_conf_file
	if [ "$use_conf_file" = 1 ]; then
		append_arg $1 config_file "-c"
	else
		append_arg $1 server "-s"
		append_arg $1 server_port "-p"
		append_arg $1 password "-k"
		append_arg $1 encrypt_method "-m"
	fi
	[ -z "$args" ] && return 2
	append_arg $1 tunnel_port "-l"
	append_arg $1 tunnel_forward "-L"
	eval "service_start /usr/bin/ss-tunnel $args -u"
	return $?
}

start() {
	config_load shadowsocks
	config_foreach start_rules shadowsocks && \
	config_foreach start_redir shadowsocks
	config_foreach start_tunnel shadowsocks
}

stop() {
	/usr/bin/ss-rules -f && \
	service_stop /usr/bin/ss-redir
	service_stop /usr/bin/ss-tunnel
}

rules() {
	config_load shadowsocks
	config_foreach start_rules shadowsocks
}
