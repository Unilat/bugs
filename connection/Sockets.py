'''
Created: Novemeber 1, 2001

@Author: Paul Schwendenman
'''
# * * * * * * *
# * Imported  *
# * * * * * * *
import socket
from cPickle import dumps, loads


# * * * * * * *
# * Classes   *
# * * * * * * *
class Connection():
    '''
    The base for a client and server connection
    '''
    def __init__(self, address=None, port=5000):
        self.server_socket = socket.socket(socket.AF_INET,
                                             socket.SOCK_STREAM)
        self.address = address
        self.port = port
        self.socket = None

    def send(self, data):
        '''
        Sends the data to the remote connection
        '''
        data = dumps(data)
        self.socket.send(data)

    def recv(self):
        '''
        Recieves the data from the remote connection
        '''
        data = self.socket.recv(4096)
        data = loads(data)
        return data

    def openSocket(self):
        '''
        Binds a connection to a specific address and port
        '''
        if self.address == None:
            raise ValueError("No Address")
        else:
            print self.address
        self.server_socket.bind((self.address, self.port))

    def close(self):
        '''
        Closes the connection in a timely fasion
        '''
        if self.socket != None:
            self.socket.shutdown(socket.SHUT_RDWR)  # Timely fasion
            self.socket.close()  # Close
            self.socket = None

    def __del__(self):
        '''
        Some nasty stuff happens if you don't close the connections properly
        mostly you have to wait a while until the connection closes on its
        own.
        '''
        self.close()


class ServerConnection(Connection):
    '''
    Sets up a connection as a server
    '''
    def __init__(self, port=5000):
        '''
        Sets up a server connection to accept from all addresses i.e. ""
        '''
        self.server_socket = socket.socket(socket.AF_INET,
                                             socket.SOCK_STREAM)
        self.address = ""
        self.port = port
        self.socket = None

    def listen(self):
        '''
        Listens for five connection requests to be handled by acceptConnection
        '''
        self.server_socket.listen(5)

    def openSocket(self):
        '''
        Binds a connection to a specific address and port
        '''
        if self.address == None:
            raise ValueError("No Address")
        else:
            print self.address
        self.server_socket.bind((self.address, self.port))

    def acceptConnection(self):
        '''
        Accepts a connection from a client returns address
        '''
        self.socket, address = self.server_socket.accept()
        return address


class ClientConnection(Connection):
    '''
    Sets up a connection as a client
    '''
    def __init__(self, address, port=5000):
        self.socket = socket.socket(socket.AF_INET,
                                      socket.SOCK_STREAM)
        self.address = address
        self.port = port

    def openSocket(self):
        '''
        Connects a connection to a specific address and port
        '''
        if self.address == None:
            raise ValueError("No Address")
        else:
            print self.address
        self.socket.connect((self.address, self.port))


def startServer(port):
    '''
    Sample of how you would start a server side connection
    '''
    temp = ServerConnection(port)
    print temp.address
    temp.openSocket()
    temp.listen()
    return temp


def startClient(address, port):
    '''
    Sample of how you would start a client side connection
    '''
    temp = ClientConnection(address, port)
    temp.openSocket()
    return temp


def main():
    '''
    This is how the module should be used in theory
    however I believe this example will fail
    because a system cannot open two sockets to the same thing
    '''
    try:
        connection1 = startServer(5001)
        connection2 = startClient('localhost', 5001)
        data = [123, 324, 443, 435, 234]
        connection1.send(data)
        newdata = connection2.recv()
        connection1.close()
    finally:
        del connection1
        del connection2
    assert data == newdata
