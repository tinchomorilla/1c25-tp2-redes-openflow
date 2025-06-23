#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.packet import ethernet

from pox.custom.firewall import Firewall

log = core.getLogger()


class Controller:
    def __init__(self, connection, rules, firewall_switch=None):
        self.connection = connection
        self.mac_to_port = {}
        # Initialize firewall to install rules in switches
        self.firewall = Firewall(rules, firewall_switch)
        connection.addListeners(self)
        log.info("Switch connected: %s", connection)

    def _handle_PacketIn(self, event):
        packet = event.parsed
        inport = event.port

        if not packet.parsed:
            log.warning("Malformed packet, discarded")
            return

        src_mac = str(packet.src)
        dst_mac = str(packet.dst)
        self.mac_to_port[src_mac] = inport

        # Normal learning switch behavior
        if dst_mac in self.mac_to_port:
            outport = self.mac_to_port[dst_mac]
            log.info("📤 Forwarding packet to port %d (known MAC)", outport)
        else:
            outport = of.OFPP_FLOOD
            log.info("📤 Forwarding packet by FLOOD (unknown MAC)")

        msg = of.ofp_packet_out()
        msg.data = event.ofp
        msg.in_port = inport
        msg.actions.append(of.ofp_action_output(port=outport))
        event.connection.send(msg)
