#!/usr/bin/env python2

from mininet.topo import Topo
import argparse

class LinearTopology(Topo):
    def __init__(self, n_switches=3):
        # Initialize topology
        Topo.__init__(self)

        # Add hosts
        host1 = self.addHost('h1')
        host2 = self.addHost('h2')

        # Add switches
        switches = []
        for i in range(n_switches):
            switches.append(self.addSwitch('s%d' % (i+1)))

        # Add links
        # Connect host1 to first switch
        self.addLink(host1, switches[0])
        
        # Connect switches in a chain
        for i in range(n_switches - 1):
            self.addLink(switches[i], switches[i + 1])
        
        # Connect last switch to host2
        self.addLink(switches[-1], host2)

def main():
    parser = argparse.ArgumentParser(description='Create a linear topology with n switches')
    parser.add_argument('n_switches', type=int, help='Number of switches in the chain')
    args = parser.parse_args()

    # Create topology
    topo = LinearTopology(n_switches=args.n_switches)
    print("Created linear topology with %d switches" % args.n_switches)

if __name__ == '__main__':
    main()