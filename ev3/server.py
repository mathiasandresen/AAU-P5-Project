import socket
from time import sleep
from sys import exit

PORT_RANGE = (1234, 1235, 1236, 1237, 1238)

class Server:
    '''Server socket class'''

    def __init__(self, host):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host

    def start_server(self):          
        for port in PORT_RANGE:
            try:
                print("Trying server on '%s:%s'" % (self.host, port))
                self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.server_socket.bind((self.host, port))
                self.server_socket.listen(1)
                print("Server started on '%s:%s'!" % (self.host, port))
                return
            except OSError as error:
                print("Could not start on %i" % port)
                sleep(1)
        print("Could not start server on any port")
        sleep(1)
        exit("Could not bind to any port")

    def wait_for_connection(self):
        while True:
            self.connection, self.client_address = self.server_socket.accept()
            if self.connection:
                print("Connection from ", self.client_address)
                return

    def send_data_to_client(self, message):
        assert(self.connection)
        self.connection.send(message.encode())

    def wait_for_data(self):
        assert self.connection
        print("assert complete")
        try:
            while True:
                print("start receiving data")
                data = self.connection.recv(16) 
                print("Received %s" % data.decode())

                if data:
                    return self.parse_data(data.decode())
                else:
                    print("No more data")
                    break
        except Exception:
            self.connection.close()

    def parse_data(self, data):
        print("data: " + data)
        strings = data.split(",")
        assert(len(strings) == 3)
        print(strings)
        return (float(strings[0]), float(strings[1]), float(strings[2]))
