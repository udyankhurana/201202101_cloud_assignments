#!/usr/bin/python
"""
Mininet Assignment
Name: Udyan Khurana
Roll No.: 201202101
"""

import sys
from mininet.net import Mininet
from mininet.node import OVSController
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel, info

def customTopo():
    args = (sys.argv)
    num_switches = int(args[1])
    hosts_per_switch = int(args[2])
    total_hosts = num_switches * hosts_per_switch
    odd_ip = '11.0.0.'
    even_ip = '11.0.1.'
    even_ctr = 1
    odd_ctr = 1

    net = Mininet(controller=OVSController,link=TCLink)
    info( '*** Adding controller\n' )
    net.addController('c0')

    hosts=[]
    info( '*** Adding hosts\n' )
    for i in range(1,total_hosts+1):
        if i%2 == 1:
            hosts.append(net.addHost('h'+str(i), ip=odd_ip+str(odd_ctr)+'/24'))
            odd_ctr+=1
        else:
            hosts.append(net.addHost('h'+str(i), ip=even_ip+str(even_ctr)+'/24'))
            even_ctr+=1

    switches=[]
    info( '*** Adding switches\n' )
    for i in range(1,num_switches+1):
        switches.append(net.addSwitch('s'+str(i)))

    info( '*** Making Links\n' )
    # Linking Hosts and Switches
    host_no=0
    for i in range(num_switches):
        for j in range(hosts_per_switch):
            bandwidth=(host_no%2)+1
            net.addLink(switches[i], hosts[i*hosts_per_switch + j], bw=bandwidth) # Odd Host = 1 mbps, Even Host = 2 mbps
            print " [h" + str(i*hosts_per_switch + j + 1) + "<--> s" + str(i+1) + "]"
            host_no+=1

    # Linking all Switches
    for i in range(num_switches-1):
        net.addLink(switches[i], switches[i+1], bw=2) # Switch Bandwidth (2 mbps)
        print " [s" + str(i+1) + "<--> s" + str(i+2) + "]"
#    net.addLink(switches[num_switches-1], switches[0], bw=2)
#    print " [s" + str(num_switches) + "<--> s1]"

    info( '*** Starting the Network and CLI\n' )
    net.start()
    CLI(net)

    info( '*** Adding controller\n' )
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    customTopo()
