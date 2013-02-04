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

def sendBugLanguageCode(address, data, port=5000):
    '''
    This would be used to send the compiled code to the server.
    '''
    try:
        connect = Sockets.ClientConnection(address, port)
        connect.openSocket()
    except:
        handleError()
    else:
        connect.send(data)
        callback = connect.recv()
    finally:
        connect.close()
    return callback == data

#Testing
send = sendBugLanguageCode


def main():
    print  "Enter Data:"
    data = raw_input("> ")
    send('sarcasm.ath.cx', data, 54363)


if __name__ == "__main__":
    main()
