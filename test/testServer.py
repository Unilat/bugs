
# Echo client program
import socket
from cPickle import dumps, loads

address = 'sarcasm.ath.cx'    # The remote host
port = 54363              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((address, port))
data = dumps('Hello, world')
s.send(data)
data2 = s.recv(4096)
s.close()
print 'Received', repr(loads(data2))
try:
    assert data == data2
except:
    print "Fail"
else:
    print "Pass"
