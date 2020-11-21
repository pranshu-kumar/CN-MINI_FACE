'''
Python code to define Multi-Threaded Server

CLIENT REQUEST MESSAGE:
------------------------
req_msg = {
    command: "LOGIN/LOGOUT/FETCH...",
    header_lines: {
        server_id: server_id,
        accept_encoding: 'utf-8',
        ... 
    },
    body: 'data'
}

SERVER RESPONSE MESSAGE:
------------------------
response_msg = {
    status_line: {
        protocol: 'TCP/UDP',
        status_code: 200/301...
    },
    header_lines: {
        date: date,
        accept_ranges: bytes,
        content_length: content_length,
        keep_alive: {
            timeout: 10,
            max: 100
        },
        connection: 'keep-alive'
    }
    data: data
}
'''

import socket
from _thread import *
import threading
import pickle

from database import user_login, user_register

print_lock = threading.Lock()

# Client Request Message
client_req_msg = {
    "command": "",
    "header_lines": {
        "server_id": 12345,
        "accept_encoding": 'utf-8',
    },
    "body": ""
}

# Server Response Message
server_response_msg = {
    "status_line": {
        "protocol": 'TCP',
        "status_code": 1
    },
    "header_lines": {
        "date": "",
        "accept_ranges": bytes,
        "content_length": 0,
        "keep_alive": {
            "timeout": 10,
            "max": 100
        },
        "connection": 'keep-alive'
    },
    "data": ""
}


class Server():
    def __init__(self, PORT, host):
        self.PORT = PORT
        self.host = host

    '''
    Create a server socket
    '''
    def create_server_socket(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Server Socket Created!")
        return self.server_socket


    '''
    Bind Socket
    '''
    def bind_server_socket(self):   
        self.server_socket.bind((self.host, self.PORT))
        print("Socket Binded to port {}!".format(self.host))

    '''
    Socket Listening
    '''
    def server_socket_listen(self):
        self.server_socket.listen(5)
        print("Server Socket is listening")


    '''
    Server Socket Accept
    '''
    def server_socket_accept(self):
        # Establish connection with client
        client, addr = self.server_socket.accept()

        # Client acquires lock
        print_lock.acquire()
        print("Connected to client: ", addr[0])
        return client, addr

    '''
    Connect with Clients and perform Send and Receive
    '''
    def connect_to_clients(self):
        while(1):
            
            client, addr = self.server_socket_accept()
            
            # Perform Threaded Send and Receive
            start_new_thread(self.server_snd_and_rcv, (client,))

        self.server_socket.close()

    '''
    Server side send and receive
    '''
    def server_snd_and_rcv(self, client):
        while(1):
            # Send and Receive
            # Necessary functions for sending and accepting req/response to be added here
            request = client.recv(1024)
            if request:
                print("object in bytes: ", request)
                client_req = pickle.loads(request, encoding='utf-8')
                print(client_req)
            else:
                break
        client.close()