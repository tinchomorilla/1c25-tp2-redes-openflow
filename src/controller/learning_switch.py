from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()


class LearningSwitch(object):
    def __init__(self, connection):
        # Guarda la conexión con el switch
        self.connection = connection

        # Tabla MAC → puerto
        self.mac_to_port = {}

        # Conectamos el manejador de eventos
        connection.addListeners(self)
        log.info("LearningSwitch conectado: %s", connection)

    def _handle_PacketIn(self, event):
        packet = event.parsed
        inport = event.port

        if not packet.parsed:
            log.warning("Paquete malformado ignorado")
            return

        src_mac = str(packet.src)
        dst_mac = str(packet.dst)

        # Aprendizaje: MAC origen → puerto
        self.mac_to_port[src_mac] = inport
        log.debug("Aprendido: %s está en el puerto %d", src_mac, inport)

        if dst_mac in self.mac_to_port:
            # Si el switch ya sabe dónde está la MAC destino, 
            # reenvía el paquete directamente a ese puerto.
            outport = self.mac_to_port[dst_mac]
            log.debug("Enviando de %s a %s por el puerto %d", src_mac, dst_mac, outport)
        else:
            # Comportamiento de un switch real la primera vez que ve un destino.
            outport = of.OFPP_FLOOD
            log.debug("Destino %s desconocido, FLOOD", dst_mac)

        # Construir un mensaje OpenFlow
        # Le dice al switch: “reenviá este paquete por el puerto X”.
        msg = of.ofp_packet_out()
        msg.data = event.ofp
        msg.actions.append(of.ofp_action_output(port=outport))
        msg.in_port = inport
        event.connection.send(msg)


# Función de arranque del módulo
def launch():
    def start_switch(event):
        log.info("Conexión entrante: %s", event.connection)
        LearningSwitch(event.connection)
    
    core.openflow.addListenerByName("ConnectionUp", start_switch)
