import os
import sys
import logging
import subprocess
from optparse import OptionParser

# import subprocess
# >>> result = subprocess.run(['ls', '-l'], stdout=subprocess.PIPE)
# >>> result.stdout
# os.system('gnome-terminal -- ping 8.8.8.8')

class VemolWare:
    def __init__(self):
        self.logger = logging.getLogger('spam_application.auxiliary.Auxiliary')

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
        # if len(self.args) != 1 or self.options.interface == None:
        #     parser.print_help()
        #     sys.exit(0)
        
        # Check ipforwarding is OK
        # if subprocess.run(['echo', '1', '>', '/proc/sys/net/ipv4/ip_forward'], stdout=subprocess.PIPE).returncode != 0:
        #     error = 'Failed to ipfowarding'
        #     # loggin.error(error)
        #     sys.exit(0)

        # Select target domain
        try:
            print("\nEnter the domain:")
            print("[1] - Gmail.")
            print("[2] - Outlook.")
            print("[3] - Other.\n\n")
            option_domain = int(input("Selected option: "))
            if option_domain == 3:
                new_domain = input("\n\nEnter your domain: ")
                # TODO: wget para el domain
        except ValueError:
            print("Sorry, I didn't understand that.")
            sys.exit(0)


    def check_requirements(self):
        pass
        # os.system('gnome-terminal -- ping 8.8.8.8')

    def arpspoof(self, interface, target):
        pass
        # os.system('gnome-terminal -- arpspoof -i 'eth0' -t 'local_ip' 'target_router')
    
    def dnssniff (self, hosts_file):
        pass
        # os.system('gnome-terminal -- ping 8.8.8.8')
    
    def flask_server (self, target):
        # Starting Flask server targeting domain address
        os.system('gnome-terminal -- python3 code/app.py')

if __name__ == "__main__":
    arpspoof = VemolWare()
	# arpspoof.main()



