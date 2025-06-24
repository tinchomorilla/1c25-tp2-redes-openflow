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
        # Start HTTP server on h3
        makeTerm(self.net.get("h3"), cmd="bash -c 'iperf -s -u -p 80; exec bash'")
        time.sleep(5)
        # Start iperf client on h2
        makeTerm(
            self.net.get("h1"), cmd="bash -c 'iperf -c 10.0.0.3 -u -p 80; exec bash'"
        )

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
        # Start iperf server on h3
        makeTerm(self.net.get("h3"), cmd="bash -c 'iperf -s -u -p 5001; exec bash'")
        # Wait for server to start
        time.sleep(5)
        # Start iperf client on h2
        makeTerm(
            self.net.get("h2"), cmd="bash -c 'iperf -c 10.0.0.3 -u -p 5001; exec bash'"
        )

    def test_connectivity(self):
        """Test basic connectivity between all hosts using pingAll."""
        logger.info("Testing connectivity between all hosts with pingAll...")
        result = self.net.pingAll()
        logger.info("pingAll result: %s", result)
