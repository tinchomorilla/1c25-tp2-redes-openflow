#!/usr/bin/env python2
# -*- coding: utf-8 -*-

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
from src.topologies.linear_topology import LinearTopology

logger = setup_logger(__name__)


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Topología lineal con controlador remoto"
    )
    parser.add_argument("n", type=int, help="Cantidad de switches")
    parser.add_argument(
        "--rule",
        "-r",
        type=str,
        choices=["R1", "R2", "R3"],
        help="Regla a probar (R1: HTTP, R2: UDP, R3: h2-h3)",
    )
    return parser.parse_args()


def create_network(n_switches):
    """Create and start the Mininet network."""
    logger.info("Creando topología lineal con %d switches", n_switches)
    topo = LinearTopology(n=n_switches)

    logger.info("Iniciando red Mininet con controlador remoto en 127.0.0.1:6633")
    net = Mininet(
        topo=topo,
        controller=lambda name: RemoteController(name, ip="127.0.0.1", port=6633),
    )

    net.start()
    return net


def log_network_info():
    """Log network configuration information."""
    logger.info("IPs configuradas:")
    logger.info("h1: 10.0.0.1")
    logger.info("h2: 10.0.0.2")
    logger.info("h3: 10.0.0.3")
    logger.info("h4: 10.0.0.4")


def run_rule_test(net, rule):
    """Run the specified rule test if a rule is provided."""
    if not rule:
        return

    rule_tester = RuleTester(net)
    test_methods = {
        "R1": rule_tester.test_first_rule,
        "R2": rule_tester.test_second_rule,
        "R3": rule_tester.test_third_rule,
    }

    test_method = test_methods.get(rule)
    if test_method:
        test_method()


def cleanup_resources():
    """Clean up Mininet resources."""
    try:
        os.system("sudo mn -c")
        logger.info("Limpieza de recursos completada")
    except Exception as e:
        logger.error("No se pudo realizar la limpieza de recursos: %s", str(e))


def main():
    """Main function to run the linear topology."""
    try:
        # Parse command line arguments
        args = parse_arguments()
        setLogLevel("info")

        # Create and start network
        net = create_network(args.n)
        log_network_info()

        # Run rule test if specified
        run_rule_test(net, args.rule)

        # Start Mininet CLI
        CLI(net)

        # Cleanup
        logger.info("Deteniendo red...")
        net.stop()
        cleanup_resources()

    except Exception as e:
        logger.error("Error durante la ejecución: %s", str(e))
        cleanup_resources()
        raise


if __name__ == "__main__":
    main()
