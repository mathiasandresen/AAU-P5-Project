'''Module handling the client side of the server/client socket connection'''
import socket


class Client:
    '''A client socket class'''

    def __init__(self, host, port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (host, port)
        self.connection = None
    # END

    def connect_to_server(self):
        '''Creates a connection to the specified server'''
        self.connection = self.client_socket.connect(self.server_address)

    def wait_for_string(self, string):
        '''Waits until the specified string is received'''
        while True:
            data = self.client_socket.recv(16).decode()
            print("Received %s, expected %s" % data, string)
            assert data == string
            break

    def send_data_to_server(self, data):
        '''Sends data to the server'''
        assert self.connection is not None
        self.connection.send(data.encode())