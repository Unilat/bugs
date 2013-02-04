'''
Created: 5 Nov 2011

@Author: Paul Schwendenman
'''

# Echo server program
import socket
from cPickle import loads, dumps

address = ''                 # Symbolic name meaning all available interfaces
port = 50007              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((address, host))
s.listen(1)
conn, addr = s.accept()
print 'Connected by', addr
try:
    while 1:
        data = loads(conn.recv(4096))
        if not data: break
        conn.send(dumps(data))
        print data
except:
    pass
conn.close()
            