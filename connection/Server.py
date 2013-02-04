'''
Created: Novemeber 2, 2001

@Author: Paul Schwendenman
'''
# * * * * * * *
# * Imported  *
# * * * * * * *
import Sockets
from handleError import *

# * * * * * * *
# * Functions *
# * * * * * * *

def recieveBugLanguageCode(port=54363):
    '''
    Theorectically this could be called by program to get code from clients.
    Possibly more filled out 
    '''
    data = None
    try:
        connect = Sockets.ServerConnection(port)
        connect.openSocket()
        connect.listen()
        connect.acceptConnection()
        data = connect.recv()
    except:
        handleError()
    finally:
        connect.close()
    return data

def sendDisplays(port=54363):
    data = None
    try:
        connect = Sockets.ServerConnection(port)
        connect.openSocket()
        connect.listen()
        connect.acceptConnection()
        grids = [[23,43,21,30,],[43,0,0,0,],[62,0,0,0],
        [0,52,0,43,22,21,0, 0, 0,0, 0, 0, 0,63,0, 0,0, 0, 41, 22,0,0, 0,0, 0, 0, 0,50, 0, 0,0, 0, 0, 0,0,0, 0,0,21, 0, 0,0,0, 62,0, 0, 0,40,0,],
        [0,0,0,23,23,21,0,52, 0,0, 0, 0, 0,63,0, 0,0, 0, 41, 42,0,0, 0,0, 0, 0, 0,50, 0, 0,0, 0, 0, 0,0,0, 0,0,22, 0, 0,0,0, 60,0, 0, 0,40,0,],
        [0,0,0,43,23,21,0,51, 0,0, 0, 0, 0,63,0, 0,0, 0, 42, 42,0,0, 0,0, 0, 0, 0,50, 0, 0,0, 0, 0, 0,0,0, 0,0,22, 0, 0,0,0, 63,0, 0, 0,40,0,],
        [0,0,0,43,23,21,0, 0,51,0, 0, 0, 0,63,0, 0,0, 0, 41, 43,0,0, 0,0, 0, 0, 0,50, 0, 0,0, 0, 0, 0,0,0, 0,0,21, 0, 0,0,0, 61,0, 0, 0,40,0,],]
        for data in grids:
            connect.send(data)
            connect.recv()
    except:
        handleError()
    finally:
        print "Close"
        connect.close()
    

#Testing
get = recieveBugLanguageCode



def main():
    print "Data:"
    data = get()
    print data

if __name__ == "__main__":
    #main()
    sendDisplays()
