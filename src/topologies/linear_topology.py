#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.log import setLogLevel
from mininet.cli import CLI
import argparse
import os
import time
from mininet.term import makeTerm

from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class LinearTopology(Topo):
    def build(self, n=3):
        logger.info("Iniciando construcción de topología lineal con %d switches", n)
        # Set IPs for hosts
        host1 = self.addHost("h1", ip="10.0.0.1/24")
        host2 = self.addHost("h2", ip="10.0.0.2/24")
        host3 = self.addHost("h3", ip="10.0.0.3/24")
        host4 = self.addHost("h4", ip="10.0.0.4/24")
        switches = []

        # Crear switches
        for i in range(n):
            switch = self.addSwitch("s%d" % (i + 1))
            switches.append(switch)
            logger.debug("Switch s%d creado", i + 1)

        # Conectar hosts al primer switch (h1 y h2)
        self.addLink(host1, switches[0])
        self.addLink(host2, switches[0])
        logger.debug("Hosts h1 y h2 conectados al switch s1")

        # Conectar hosts al último switch (h3 y h4)
        self.addLink(host3, switches[-1])
        self.addLink(host4, switches[-1])
        logger.debug("Hosts h3 y h4 conectados al switch s%d", n)

        # Conectar switches en cadena
        for i in range(n - 1):
            self.addLink(switches[i], switches[i + 1])
            logger.debug("Switch s%d conectado al switch s%d", i + 1, i + 2)

        logger.info("Topología lineal construida exitosamente")


def main():
    try:
        parser = argparse.ArgumentParser(
            description="Topología lineal con controlador remoto"
        )
        parser.add_argument("n", type=int, help="Cantidad de switches")
        args = parser.parse_args()

        setLogLevel("info")  # Podés cambiar a 'debug' si querés más detalle

        logger.info("Creando topología lineal con %d switches", args.n)
        topo = LinearTopology(n=args.n)

        # Crear la red con controlador remoto (por default IP localhost)
        logger.info("Iniciando red Mininet con controlador remoto en 127.0.0.1:6633")
        net = Mininet(
            topo=topo,
            controller=lambda name: RemoteController(name, ip="127.0.0.1", port=6633),
        )

        net.start()
        logger.info("Red iniciada exitosamente con %d switches", args.n)
        logger.info("IPs configuradas:")
        logger.info("h1: 10.0.0.1")
        logger.info("h2: 10.0.0.2")
        logger.info("h3: 10.0.0.3")
        logger.info("h4: 10.0.0.4")
        logger.info("Para probar las reglas del firewall:")
        logger.info("1. HTTP (puerto 80): h2 python -m SimpleHTTPServer 80")
        logger.info("2. UDP puerto 5001: h1 iperf -s -u -p 5001")
        logger.info("3. Comunicación h2-h3: ping 10.0.0.3")

        # Abrir xterm para h3 (servidor) y ejecutar iperf server
        makeTerm(net.get("h3"), cmd="bash -c 'iperf -s -u -p 5001; exec bash'")

        # Esperar 5 segundos para que el servidor inicie
        time.sleep(5)

        # Abrir xterm para h1 (cliente) y ejecutar iperf client
        makeTerm(net.get("h1"), cmd="bash -c 'iperf -c 10.0.0.3 -u -p 5001; exec bash'")

        CLI(net)  # Entra en la CLI de Mininet

        logger.info("Deteniendo red...")
        net.stop()

        # Limpiar interfaces y procesos de Mininet
        logger.info("Limpiando recursos de Mininet...")
        os.system("sudo mn -c")
        logger.info("Limpieza completada")

    except Exception as e:
        logger.error("Error durante la ejecución: %s", str(e))
        # Intentar limpiar recursos en caso de error
        try:
            os.system("sudo mn -c")
            logger.info("Limpieza de recursos completada después del error")
        except:
            logger.error("No se pudo realizar la limpieza de recursos")
        raise


if __name__ == "__main__":
    main()
