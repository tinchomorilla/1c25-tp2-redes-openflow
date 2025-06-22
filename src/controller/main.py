#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from pox.core import core
import json

from pox.switch_controller import Controller

log = core.getLogger()


def launch(rules_path="pox/rules.json"):
    """
    Launch function for POX.
    This is the entry point that POX will call when starting the controller.
    """

    def start_switch(event):
        """Handle new switch connections."""
        try:
            with open(rules_path, "r") as f:
                config = json.load(f)
            firewall_switch = config.get("firewall_switch")
            rules = (
                config["rules"] if "rules" in config else config
            )  
            Controller(event.connection, rules, firewall_switch)
        except Exception as e:
            log.error("Error starting controller: %s", str(e))
            raise

    core.openflow.addListenerByName("ConnectionUp", start_switch)
    log.info("🔥 Controller started")
