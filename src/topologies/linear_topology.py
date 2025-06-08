#!/usr/bin/env python2

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.log import setLogLevel
from mininet.cli import CLI
import argparse
import os


class LinearTopology(Topo):
    def build(self, n=3):
        host1 = self.addHost("h1")
        host2 = self.addHost("h2")
        switches = []

        # Crear switches
        for i in range(n):
            switch = self.addSwitch("s%d" % (i + 1))
            switches.append(switch)

        # Conectar host1 al primer switch
        self.addLink(host1, switches[0])

        # Conectar switches en cadena
        for i in range(n - 1):
            self.addLink(switches[i], switches[i + 1])

        # Conectar último switch al host2
        self.addLink(switches[-1], host2)


def main():
    parser = argparse.ArgumentParser(
        description="Topología lineal con controlador remoto"
    )
    parser.add_argument("n", type=int, help="Cantidad de switches")
    args = parser.parse_args()

    setLogLevel("info")  # Podés cambiar a 'debug' si querés más detalle

    topo = LinearTopology(n=args.n)

    # Crear la red con controlador remoto (por default IP localhost)
    net = Mininet(
        topo=topo,
        controller=lambda name: RemoteController(name, ip="127.0.0.1", port=6633),
    )

    net.start()
    print("*** Red iniciada con %d switches" % args.n)
    print("*** Ejecutá 'pingall' para probar conectividad o inspeccioná con Wireshark")
    CLI(net)  # Entra en la CLI de Mininet
    net.stop()

    # Limpiar interfaces y procesos de Mininet
    os.system("sudo mn -c")


if __name__ == "__main__":
    main()
