__author__ = 'Eric'

import socket
import cPickle
import pprint
import message

SERVER_ADDRESS = ('localhost', 8000)
SOCKET_TIMEOUT = 3


class Logon_Client(object):

    login_prompt = ('Username: ', 'Password: ')

    def __init__(self):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.settimeout(SOCKET_TIMEOUT)

        try:
            self.connection.connect(SERVER_ADDRESS)
        except socket.error:
            print 'connection failed'
            exit(1)
        else:
            self.wfile = self.connection.makefile('wb', 0)
            self.rfile = self.connection.makefile('rb', -1)
            print'socket created with read and write file interface'
            print self.rfile
            response = self.receive()
            if response.type == 'ack':
                print 'received server acknowledgement'
            else:
                raise socket.error



    def send(self, to_server):
        cPickle.dump(to_server, self.wfile)

    #put error methods here
    def receive(self):
        try:
            return cPickle.load(self.rfile)
        except socket.timeout as e:
            print 'socket timeout: %s' % e
        except EOFError as e:
            print 'no pickle sent to load: %s' % e

    def login(self):

        while True:
            username = raw_input(Logon_Client.login_prompt[0])
            password = raw_input(Logon_Client.login_prompt[1])

            self.send(message.Message('login', [username, password]))


            response = self.receive()
            if (response.data[0] == 's'):
                print 'login success: %s' % response
                return True
            elif (response.data[0] == 'u'):
                print 'wrong username: %s' % response
            elif (response.data[0] == 'p'):
                print 'wrong password: %s' % response
            else:
                print 'login failed'
                print response
                return False


    def handle(self):

        response = self.receive()

        while(response.type != 'close'):
            pass


if __name__ == '__main__':
    client = Logon_Client()
    if (client.login()):
        print 'login successful'
        client.handle()
    else:
        print 'login fail'









