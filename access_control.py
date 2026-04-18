from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

# Allow only h1 <-> h2
ALLOWED_IP_PAIRS = {
    ("10.0.0.1", "10.0.0.2"),
    ("10.0.0.2", "10.0.0.1"),
}

# Learn MAC -> port per switch
mac_to_port = {}

def _handle_PacketIn(event):
    packet = event.parsed
    if not packet.parsed:
        return

    dpid = event.connection.dpid
    in_port = event.port

    # Initialize learning table for this switch
    if dpid not in mac_to_port:
        mac_to_port[dpid] = {}

    # Learn source MAC location
    mac_to_port[dpid][packet.src] = in_port

    # Always allow ARP so hosts can resolve addresses
    if packet.type == packet.ARP_TYPE:
        msg = of.ofp_packet_out()
        msg.data = event.ofp
        msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
        event.connection.send(msg)
        return

    ip_packet = packet.find('ipv4')
    if ip_packet is None:
        return

    src_ip = str(ip_packet.srcip)
    dst_ip = str(ip_packet.dstip)

    log.info(f"Packet: {src_ip} -> {dst_ip}")

    # Block anything not in the whitelist
    if (src_ip, dst_ip) not in ALLOWED_IP_PAIRS:
        log.info("BLOCKED")
        return

    # Allowed traffic
    out_port = mac_to_port[dpid].get(packet.dst, of.OFPP_FLOOD)

    # Install flow rule
    flow_mod = of.ofp_flow_mod()
    flow_mod.match = of.ofp_match.from_packet(packet, in_port)
    flow_mod.actions.append(of.ofp_action_output(port=out_port))
    event.connection.send(flow_mod)

    # Send current packet
    packet_out = of.ofp_packet_out()
    packet_out.data = event.ofp
    packet_out.actions.append(of.ofp_action_output(port=out_port))
    event.connection.send(packet_out)

    log.info("ALLOWED")

def _handle_ConnectionUp(event):
    log.info("Switch connected")
    event.connection.addListenerByName("PacketIn", _handle_PacketIn)

def launch():
    core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
