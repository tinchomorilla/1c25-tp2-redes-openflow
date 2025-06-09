#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import pox.openflow.libopenflow_01 as of
from pox.lib.packet import tcp, udp, icmp
from pox.core import core

log = core.getLogger()


class Firewall:
    def __init__(self, rules):
        self.rules = rules
        log.info("Loaded rules: %s", rules)
        # Install rules proactively when firewall is initialized
        self._install_all_rules()

    def _install_all_rules(self):
        """Install all firewall rules in all switches."""
        for conn in core.openflow.connections:
            for rule in self.rules:
                self._install_rule(conn, rule)

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
            "🔒 Installed rule %s in switch %s",
            rule["rule"],
            connection.dpid,
        )

    def process_packet(self, packet, connection):
        """Process a packet and check if it matches any rules."""
        ip = packet.find("ipv4")
        if not ip:
            return False

        src_ip = str(ip.srcip)
        dst_ip = str(ip.dstip)

        # Get protocol and port information if available
        l4 = packet.find("tcp") or packet.find("udp") or packet.find("icmp")
        dst_port = l4.dstport if l4 and hasattr(l4, "dstport") else None
        proto = (
            "TCP"
            if isinstance(l4, tcp)
            else (
                "UDP"
                if isinstance(l4, udp)
                else "ICMP" if isinstance(l4, icmp) else None
            )
        )

        # Log packet information
        if isinstance(l4, icmp):
            log.info(
                "📦 ICMP Packet detected - Type: %d, Code: %d, IP src: %s, IP dst: %s",
                l4.type,
                l4.code,
                src_ip,
                dst_ip,
            )
        else:
            log.info(
                "📦 Packet detected - IP src: %s, IP dst: %s, Proto: %s, Port: %s",
                src_ip,
                dst_ip,
                proto or "N/A",
                str(dst_port) if dst_port else "N/A",
            )

        # First check IP-based rules (rules that only specify IPs)
        for rule in self.rules:
            # Skip rules that specify protocol or port
            if rule.get("protocol") or rule.get("dst_port"):
                continue

            log.info("🔍 Checking IP-based rule: %s", rule["rule"])
            if self._match_ip_rule(rule, src_ip, dst_ip):
                log.info("⚠️  DROP by IP-based rule: %s", rule["rule"])
                log.info("❌ Packet dropped by rule %s", rule["rule"])
                return True

        # Then check protocol-specific rules
        for rule in self.rules:
            # Skip rules that don't specify protocol or port
            if not (rule.get("protocol") or rule.get("dst_port")):
                continue

            log.info("🔍 Checking protocol-specific rule: %s", rule["rule"])
            if self._match_rule(rule, src_ip, dst_ip, proto, dst_port):
                log.info("⚠️  DROP by protocol-specific rule: %s", rule["rule"])
                log.info("❌ Packet dropped by rule %s", rule["rule"])
                return True

        return False

    def _match_ip_rule(self, rule, src_ip, dst_ip):
        """Check if a packet matches an IP-based rule."""
        log.info("Matching IP-based rule %s:", rule["rule"])
        log.info("  - Source IP check: %s == %s", rule.get("src_ip"), src_ip)
        log.info("  - Destination IP check: %s == %s", rule.get("dst_ip"), dst_ip)

        # Check IPs if specified
        if rule.get("src_ip") and rule["src_ip"] != src_ip:
            log.info("  ❌ Source IP mismatch")
            return False
        if rule.get("dst_ip") and rule["dst_ip"] != dst_ip:
            log.info("  ❌ Destination IP mismatch")
            return False

        log.info("  ✅ All IP conditions matched!")
        return True

    def _match_rule(self, rule, src_ip, dst_ip, proto, dst_port):
        """Check if a packet matches a protocol-specific rule."""
        log.info("Matching protocol-specific rule %s:", rule["rule"])
        log.info("  - Protocol check: %s == %s", rule.get("protocol"), proto)
        log.info("  - Source IP check: %s == %s", rule.get("src_ip"), src_ip)
        log.info("  - Destination IP check: %s == %s", rule.get("dst_ip"), dst_ip)
        log.info("  - Destination port check: %s == %s", rule.get("dst_port"), dst_port)

        # If rule specifies protocol, check it
        if rule.get("protocol"):
            if not proto or rule["protocol"] != proto:
                log.info("  ❌ Protocol mismatch")
                return False
        # If rule specifies port, check it
        if rule.get("dst_port"):
            if not dst_port or rule["dst_port"] != dst_port:
                log.info("  ❌ Destination port mismatch")
                return False
        # Check IPs if specified
        if rule.get("src_ip") and rule["src_ip"] != src_ip:
            log.info("  ❌ Source IP mismatch")
            return False
        if rule.get("dst_ip") and rule["dst_ip"] != dst_ip:
            log.info("  ❌ Destination IP mismatch")
            return False

        log.info("  ✅ All conditions matched!")
        return True
