from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import time
import pickle
from message import Message

# GLOBAL CONSTANTS
HOST = "localhost"
FORMAT = "utf8"
BUFSIZE = 1024
PORT = 12345
ADDR = (HOST, PORT)
MAX_CONNECTIONS = 10
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)
SENDER_SOCKET = socket(AF_INET, SOCK_STREAM)

# GLOBAL VARIABLES
clients = {}

def handle_client(client):
    """
    handling new user connections
    :param client: socket
    :return: None
    """
    # get the connection's client and name
    name = client.recv(BUFSIZE).decode(FORMAT)
    clients[name] = client
    while True:
        try:
            message = pickle.loads(client.recv(BUFSIZE))  # receiving message objects from the client
            client.send(pickle.dumps(Message("[MESSAGE RECEIVED BY SERVER]", "SERVER", message.sender_id)))  # sending response back to sender that SERVER has received message
            receiver_client = clients.get(message.receiver_id)
            try:
                receiver_client.send(pickle.dumps(message))
                client.send(pickle.dumps(Message("[MESSAGE RECEIVED BY RECEIVER]", "SERVER", message.sender_id)))  # sending response back to sender that RECEIVER has received message
            except Exception as e:
                print("[EXCEPTION]", e)
        except:
            print("[DISCONNECTED]", f"{client} disconnected")
            clients.pop(name)
            client.close()
            break


def wait_for_connections(SERVER):
    """
    actively listening for new connections
    :param SERVER:socket
    :return: None
    """
    while True:
        try:
            client, addr = SERVER.accept()
            print(f"[NEW CONNECTION] {addr} connected to the sever at {time.time()}")
            Thread(target=handle_client, args=(client,)).start()
        except Exception as e:
            print("[EXCEPTION] ", e)
            break
    print("[CRASHED] SERVER CRASHED")


if __name__ == "__main__":
    SERVER.listen(MAX_CONNECTIONS)
    print("[SERVER STARTED] Waiting for connections....")
    ACCEPT_THREAD = Thread(target=wait_for_connections, args=(SERVER,))
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()

