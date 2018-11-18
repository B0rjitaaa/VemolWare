import os
from app import *
from spoofing import *
import time
import multiprocessing


def hello():
    while True:
        time.sleep(5)
        print('Hello!')

def bye():
    while True:
        time.sleep(5)
        print('Bye!')

class VemolWare():
    def __init__(self):
        if os.geteuid() != 0:
            print ("[-] Run me as root")
            sys.exit(1)


spoofing = Spoofing()
flask_process = multiprocessing.Process(target=app.run, args=('0.0.0.0', '80', True))
spoofing_process = multiprocessing.Process(target=spoofing.main)

p1 = multiprocessing.Process(target=hello)
p2 = multiprocessing.Process(target=bye)

flask_process.start()
spoofing_process.start()
p1.start()
p2.start()


