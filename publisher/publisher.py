import socket
import time
import sys
sys.path.append('../definitions')
from typedef import *

#HOST = '127.0.0.1'   The server's hostname or IP address
#PORT = 65432         The port used by the server

if len(sys.argv) != 6:
    print("usage:", sys.argv[0], "<host> <port> <topic> <period> <file name>")
    sys.exit(1)

HOST, PORT, TOPIC, PERIOD, FILE = sys.argv[1], int(sys.argv[2]), sys.argv[3], int(sys.argv[4]), sys.argv[5]

sensor = open(FILE, "r")
lines = sensor.readlines()

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        registerMessage = 'publisher;' + TOPIC
        s.sendall(registerMessage.encode())
        time.sleep(1)
        for line in lines:
            s.sendall(line.encode())
            time.sleep(PERIOD)

except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    unregisterMessage = 'DISCONECT'
    sensor.close()