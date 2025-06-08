#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.log import setLogLevel
from mininet.cli import CLI
import argparse
import os

from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class LinearTopology(Topo):
    def build(self, n=3):
        logger.info("Iniciando construcción de topología lineal con %d switches", n)
        host1 = self.addHost("h1")
        host2 = self.addHost("h2")
        switches = []

        # Crear switches
        for i in range(n):
            switch = self.addSwitch("s%d" % (i + 1))
            switches.append(switch)
            logger.debug("Switch s%d creado", i + 1)

        # Conectar host1 al primer switch
        self.addLink(host1, switches[0])
        logger.debug("Host h1 conectado al switch s1")

        # Conectar switches en cadena
        for i in range(n - 1):
            self.addLink(switches[i], switches[i + 1])
            logger.debug("Switch s%d conectado al switch s%d", i + 1, i + 2)

        # Conectar último switch al host2
        self.addLink(switches[-1], host2)
        logger.debug("Host h2 conectado al switch s%d", n)

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
        logger.info(
            "Ejecutá 'pingall' para probar conectividad o inspeccioná con Wireshark"
        )

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
