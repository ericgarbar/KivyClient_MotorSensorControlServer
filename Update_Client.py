__author__ = 'Eric'

import socket
from cPickle import dump, load
import pprint
import message
import time
import Logon_Client


SERVER_ADDRESS = ('localhost', 9000)
SOCKET_TIMEOUT = 3

class Update_Client(Logon_Client.Logon_Client):
    UPDATE_INTERVAL = 1.0
    UPDATE_INFO = 'Displaying motor control updates every %f seconds' % UPDATE_INTERVAL
    DISPLAY_INFO_TIME = 2

    def __init__(self, *args, **kwargs):
        super(Update_Client, self).__init__(*args, **kwargs)


    def _handle(self):

        while True:
            print Update_Client.UPDATE_INFO
            time.sleep(Update_Client.DISPLAY_INFO_TIME)
            self.send(message.Message('update', ['update info']))
            self.receive()
            time.sleep(Update_Client.UPDATE_INTERVAL)





if __name__ == '__main__':
    client = Update_Client()
    if (client.login()):
        print 'login successful'
        
    else:
        print 'login fail'









