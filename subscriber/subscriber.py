import socket
import time
import sys
import selectors
import types

class Subscriber:
    def __init__(self):
        pass

    def startConnection(self, host, port, sel, topics):
        server_addr = (host, port)
        print("starting connection to", server_addr)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(server_addr)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        data = types.SimpleNamespace(addr=server_addr, inb=b"", outb=b"")
        sel.register(sock, events, data=data)
        for topic in topics:
            initMessage = 'subscriber;' + topic
            sock.sendall(initMessage.encode())
            time.sleep(1)

    def service(self, key, mask, sel):
        sock = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(1024)  # Should be ready to read
            if recv_data:
                print("received", repr(recv_data), "from broker")
            else:
                print("closing connection", data.connid)
                sel.unregister(sock)
                sock.close()



if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("usage:", sys.argv[0], "<host> <port> < list of topic>")
        sys.exit(1)

    sel = selectors.DefaultSelector()
    HOST, PORT = sys.argv[1], int(sys.argv[2])
    topics = []
    for i in range(len(sys.argv)):
        if i > 2:
            topics.append(sys.argv[i])

    subscriber = Subscriber()
    subscriber.startConnection(HOST, int(PORT), sel, topics)

    try:
        while True:
            events = sel.select(timeout=1)
            if events:
                for key, mask in events:
                    subscriber.service(key, mask, sel)
            # Check for a socket being monitored to continue.
            if not sel.get_map():
                break
    except KeyboardInterrupt:
        print("caught keyboard interrupt, exiting")
    finally:
        sel.close()