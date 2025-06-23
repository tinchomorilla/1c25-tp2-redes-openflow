#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import pox.openflow.libopenflow_01 as of
from pox.core import core

log = core.getLogger()


class Firewall:
    """
    Installs firewall rules on a specific switch (by name, e.g., 's2') or all switches if not specified.
    """

    def __init__(self, rules, firewall_switch=None):
        self.rules = rules
        self.firewall_switch = firewall_switch  # e.g., 's2' or None
        log.info("Loaded rules: %s", rules)
        if self.firewall_switch:
            log.info(
                "Firewall will be installed only on switch: %s", self.firewall_switch
            )
        else:
            log.info("Firewall will be installed on all switches.")
        core.openflow.addListenerByName("ConnectionUp", self._on_switch_up)

    def _on_switch_up(self, event):
        """Install rules on the correct switch when it connects."""
        dpid = event.connection.dpid
        switch_name = self._dpid_to_name(dpid)
        if self.firewall_switch:
            if switch_name != self.firewall_switch:
                log.info(
                    "Switch %s (dpid %s) is not the firewall switch (%s), skipping rule install.",
                    switch_name,
                    dpid,
                    self.firewall_switch,
                )
                return
            log.info(
                "Installing firewall rules on switch %s (dpid %s)", switch_name, dpid
            )
        else:
            log.info(
                "Installing firewall rules on switch %s (dpid %s)", switch_name, dpid
            )
        for rule in self.rules:
            self._install_rule(event.connection, rule)

    def _install_rule(self, connection, rule):
        """Install a single rule in a switch."""
        fm = of.ofp_flow_mod()
        fm.match.dl_type = 0x0800  # IPv4

        # Set source and destination IPs if specified
        if rule.get("src_ip"):
            fm.match.nw_src = rule["src_ip"]
        if rule.get("dst_ip"):
            fm.match.nw_dst = rule["dst_ip"]

        # Set protocol and port if specified
        if rule.get("protocol"):
            if rule["protocol"] == "TCP":
                fm.match.nw_proto = 6
            elif rule["protocol"] == "UDP":
                fm.match.nw_proto = 17
        if rule.get("dst_port"):
            fm.match.tp_dst = rule["dst_port"]

        fm.priority = 65535  # Highest priority
        fm.hard_timeout = 0  # Never expire
        fm.idle_timeout = 0  # Never expire
        # Explicitly add drop action
        fm.actions = []  # Empty actions list means drop
        connection.send(fm)
        log.info(
            "🔒 Installed rule %s in switch %s (dpid %s)",
            rule["rule"],
            self._dpid_to_name(connection.dpid),
            connection.dpid,
        )

    def _dpid_to_name(self, dpid):
        """Convert a DPID to a switch name like 's1', 's2', ..."""
        # Mininet assigns DPIDs in order, so s1 = 1, s2 = 2, ...
        return "s%d" % dpid
