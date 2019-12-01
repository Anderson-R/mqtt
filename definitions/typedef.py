class Message:
    def __init__(self, topic, message):
        self.topic = topic
        self.message = message

class singleTopic:
    def __init__(self, humidity, temperature):
        self.humidity = humidity
        self.temperature = temperature

class DoubleTopic:
    def __init__(self, humidity, celcius, fahrenheit):
        self.humidity = humidity
        self.celcius = celcius
        self.fahrenheit = fahrenheit

class Client:
    def __init__(self, addr, sock):
        self.addr = addr
        self.sock = sock


class Subscriber(Client):
    def __init__(self, addr, sock):
        super().__init__(addr, sock)
        self.topics = []

    def addTopic(self, topic):
        self.topics.append(topic)


class Publisher(Client):
    def __init__(self, addr, sock, topic):
        super().__init__(addr, sock)
        self.topic = topic
