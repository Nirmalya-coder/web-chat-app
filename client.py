from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import pickle
from message import Message

class Client:
    """
    for communication with the server
    """
    HOST = "localhost"
    PORT = 12345
    BUFSIZE = 1024
    ADDR = (HOST, PORT)
    FORMAT = "utf8"

    def __init__(self, name):
        """
        Initializing object's data members nd sending name to the server
        :param name: str
        """
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(self.ADDR)
        self.messages = []
        self.send_name(name)
        self.name = name
        receive_thread = Thread(target=self.receive_data)
        receive_thread.start()

    def receive_data(self):
        """
        Receive message objects from the server
        :return: None
        """
        while True:
            try:
                msg = pickle.loads(self.client_socket.recv(self.BUFSIZE))
                self.messages.append(msg)
                print(msg.data)
            except Exception as e:
                print("[EXCEPTION] ", e)
                break

    def send_name(self, message):
        """
        send client's name to the server
        :param message: str
        :return: None
        """
        self.client_socket.send(bytes(message, self.FORMAT))

    def send_data(self, receiver, message):
        """
        send custom objects to the server
        :param receiver: str
        :param message: object
        :return: None
        """
        data = Message(message, self.name, receiver)
        self.client_socket.send(pickle.dumps(data))

    def disconnect(self):
        """
        disconnect from the server
        :return: None
        """
        self.client_socket.close()
