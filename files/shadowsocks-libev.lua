module("luci.controller.shadowsocks-libev", package.seeall)

function index()
	if not nixio.fs.access("/etc/shadowsocks.json") then
		return
	end

	entry({"admin", "services", "shadowsocks-libev"},
		alias("admin", "services", "shadowsocks-libev", "general"),
		_("Shadowsocks"), 10)

	entry({"admin", "services", "shadowsocks-libev", "general"},
		cbi("shadowsocks-libev/shadowsocks-libev-general"),
		_("General Settings"), 10).leaf = true

	entry({"admin", "services", "shadowsocks-libev", "gfwlist"},
		call("action_gfwlist"),
		_("GFW List"), 20).leaf = true

	entry({"admin", "services", "shadowsocks-libev", "custom"},
		cbi("shadowsocks-libev/shadowsocks-libev-custom"),
		_("Custom List"), 30).leaf = true

	entry({"admin", "services", "shadowsocks-libev", "watchdog"},
		call("action_watchdog"),
		_("Watchdog Log"), 40).leaf = true
end

function action_gfwlist()
	local fs = require "nixio.fs"
	local conffile = "/etc/dnsmasq.d/dnsmasq_list.conf" 
	local gfwlist = fs.readfile(conffile) or ""
	luci.template.render("shadowsocks-libev/gfwlist", {gfwlist=gfwlist})
end

function action_watchdog()
	local fs = require "nixio.fs"
	local conffile = "/var/log/shadowsocks_watchdog.log" 
	local watchdog = fs.readfile(conffile) or ""
	luci.template.render("shadowsocks-libev/watchdog", {watchdog=watchdog})
end
