from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.packet import ethernet, ipv4, udp, tcp
import json

log = core.getLogger()


class FirewallController(object):
    def __init__(self, connection, rules):
        self.connection = connection
        self.mac_to_port = {}
        self.rules = rules
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

        # Try to get layer 3/4 information
        ip = packet.find("ipv4")
        l4 = packet.find("tcp") or packet.find("udp")

        if ip and l4:
            log.info(
                "📦 Packet detected - IP src: %s, IP dst: %s, Proto: %s, Port: %d",
                str(ip.srcip),
                str(ip.dstip),
                "TCP" if isinstance(l4, tcp) else "UDP",
                l4.dstport,
            )
            src_ip = str(ip.srcip)
            dst_ip = str(ip.dstip)
            dst_port = l4.dstport
            proto = "TCP" if isinstance(l4, tcp) else "UDP"

            for rule in self.rules:
                if self._match_rule(rule, src_ip, dst_ip, proto, dst_port):
                    log.info("⚠️  DROP by rule: %s", rule["rule"])
                    # Install rule in all switches
                    for connection in core.openflow.connections:
                        self._install_drop_rule(connection, ip, l4)
                    log.info("❌ Packet dropped by rule %s", rule["rule"])
                    return  # Don't forward this packet

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

    def _install_drop_rule(self, connection, ip, l4):
        fm = of.ofp_flow_mod()
        fm.match.dl_type = 0x0800  # IPv4
        fm.match.nw_proto = ip.protocol
        fm.match.nw_src = ip.srcip
        fm.match.nw_dst = ip.dstip
        fm.match.tp_dst = l4.dstport
        fm.priority = 65535  # Highest priority
        fm.hard_timeout = 0  # Never expire
        fm.idle_timeout = 0  # Never expire
        # Explicitly add drop action
        fm.actions = []  # Empty actions list means drop
        connection.send(fm)


    def _match_rule(self, rule, src_ip, dst_ip, proto, dst_port):
        if rule.get("protocol") and rule["protocol"] != proto:
            return False
        if rule.get("src_ip") and rule["src_ip"] != src_ip:
            return False
        if rule.get("dst_ip") and rule["dst_ip"] != dst_ip:
            return False
        if rule.get("dst_port") and rule["dst_port"] != dst_port:
            return False
        log.info("✅ Rule %s matches packet", rule["rule"])
        return True


def launch(rules_path="pox/rules.json"):
    def start_switch(event):
        with open(rules_path, "r") as f:
            rules = json.load(f)
        FirewallController(event.connection, rules)

    core.openflow.addListenerByName("ConnectionUp", start_switch)
    log.info("🔥 Firewall Controller started")
