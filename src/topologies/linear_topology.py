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
from src.topologies.rule_tester import RuleTester

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
