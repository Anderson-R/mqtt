import sys
import socket
import selectors
import types
from brokerFunctions import Broker

if len(sys.argv) != 3:
    print("usage:", sys.argv[0], "<host> <port>")
    sys.exit(1)

sel = selectors.DefaultSelector()
subscribers = []
publishers = []

host, port = sys.argv[1], int(sys.argv[2])
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
print("listening on", (host, port))
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)

try:
    broker = Broker()
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                broker.acceptClient(key.fileobj, sel)
            else:
                broker.service(key, mask, sel)
except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    sel.close()