#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from mininet.term import makeTerm
import time
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class RuleTester:
    def __init__(self, net):
        self.net = net

    def test_first_rule(self):
        """Test HTTP blocking rule (R1)"""
        logger.info("Testing HTTP blocking rule...")
        # Start HTTP server on h2
        makeTerm(
            self.net.get("h2"), cmd="bash -c 'python -m SimpleHTTPServer 80; exec bash'"
        )

        time.sleep(5)
        
        # Try to access from h1
        makeTerm(self.net.get("h1"), cmd="bash -c 'curl 10.0.0.2:80; exec bash'")

    def test_second_rule(self):
        """Test UDP blocking from h1 to port 5001 (R2)"""
        logger.info("Testing UDP blocking rule...")
        # Start iperf server on h3
        makeTerm(self.net.get("h3"), cmd="bash -c 'iperf -s -u -p 5001; exec bash'")
        # Wait for server to start
        time.sleep(5)
        # Start iperf client on h1
        makeTerm(
            self.net.get("h1"), cmd="bash -c 'iperf -c 10.0.0.3 -u -p 5001; exec bash'"
        )

    def test_third_rule(self):
        """Test blocking communication between h2 and h3 (R3)"""
        logger.info("Testing h2 to h3 blocking rule...")
        # Open terminal for h3 to see incoming packets
        makeTerm(self.net.get("h3"), cmd="bash -c 'tcpdump -i h3-eth0; exec bash'")
        # Wait for server to start
        time.sleep(5)
        # Try to ping h3 from h2
        makeTerm(self.net.get("h2"), cmd="bash -c 'ping 10.0.0.3; exec bash'")
