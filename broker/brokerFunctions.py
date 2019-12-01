import sys
import socket
import selectors
import types
sys.path.append('../definitions')
from typedef import Subscriber
from typedef import Publisher

class Broker:
    def __init__(self):
        self.SUBSCRIBE = 'subscriber'
        self.SUBACK = b'2'
        self.PUBLISHER = 'publisher'
        self.HEARTBEAT = b'4'
        self.CONNECT = b'5'
        self.CONNACK = b'6'
        self.subscribers = []
        self.publishers = []
        self.subAddr = 0

    def acceptClient(self, sock, sel):
        conn, addr = sock.accept()  # Should be ready to read
        print("new client connected: ", addr)
        conn.setblocking(False)
        data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        sel.register(conn, events, data=data)


    def service(self, key, mask, sel):
        sock = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(1024)  # Should be ready to read
            dataStr = recv_data.decode().split(';')
            if len(dataStr) == 2:
                self.register(dataStr[0], dataStr[1], data.addr, sock)
            elif recv_data:
                print("received", recv_data)
                pub = self.findPublisher(data.addr)
                if pub != None:
                    self.sendToAllRegistered(recv_data, pub.topic)
                #data.outb += recv_data
            else:
                print("closing connection to client", data.addr)
                client = self.findPublisher(data.addr)
                try:
                    if client != None:
                        self.publishers.remove(client)
                    else:
                        self.subscribers.remove(self.findSubscriber(data.addr))
                except:
                    print("unregistering client who is not subscriber neither publisher")
                sel.unregister(sock)
                sock.close()
        if mask & selectors.EVENT_WRITE:
            if data.outb:
                print("echoing", repr(data.outb), "to", data.addr)
                sent = sock.send(data.outb)  # Should be ready to write
                data.outb = data.outb[sent:]

    def register(self, kind, topic, addr, sock):
        if kind == self.SUBSCRIBE:
            sub = self.findSubscriber(addr)
            if sub == None:
                sub = Subscriber(addr, sock)
                self.subscribers.append(sub)
            sub.addTopic(topic)
            print("subscriber", addr, "registered to topics", sub.topics)

        elif kind == self.PUBLISHER:
            pub = Publisher(addr, sock, topic)
            self.publishers.append(pub)
            print("publisher", addr, "registered to topic", pub.topic)

    def findSubscriber(self, addr):
        for sub in self.subscribers:
            if sub.addr == addr:
                return sub
        return None
    
    def findPublisher(self, addr):
        for pub in self.publishers:
            if pub.addr == addr:
                return pub
        return None
    
    def sendToAllRegistered(self, message, topic):
        print("sending message to all subscribers in topic:", topic)
        for sub in self.subscribers:
            for i in range(len(sub.topics)):
                if topic == sub.topics[i]:
                    try:
                        sub.sock.sendall(message)
                        print("sendind to", sub.addr)
                    except:
                        self.subscribers.remove(sub)
