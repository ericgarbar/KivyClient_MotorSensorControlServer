__author__ = 'Eric'

__author__ = 'Eric'

import socket
from cPickle import dump, load
import pprint
import message


SERVER_ADDRESSES = (('localhost', 9000), ('localbrost', 9001))
SOCKET_TIMEOUT = 3


class Logon_Client(object):


    def __init__(self, SOCKET_TIMEOUT=SOCKET_TIMEOUT, SERVER_ADDRESSES=SERVER_ADDRESSES):
        self.connections = dict()

        for address in SERVER_ADDRESSES:
            self.connections[address[0]] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connections[address[0]].settimeout(SOCKET_TIMEOUT)

        for address in SERVER_ADDRESSES:

            try: #try to connect to server
                self.connections[address[0]].connect(address)
            except socket.error:
                print 'connection failed'
                exit(1)
            else: #create wfile for writing and rfile for reading pickled objects from
                self.wfile = self.connections[address[0]].makefile('wb', 0)
                self.rfile = self.connection[address[0]].makefile('rb', -1)
                print'socket created with read and write file interface'
                print self.rfile
                first_ack = load(self.rfile) #give acknowledgement to send password

                if first_ack.type == 'ack':
                    print 'received server acknowledgement'
                else:
                    raise socket.error



    def send(self, task_to_server):
        dump(task_to_server, self.wfile)
        acknowledgement = load(self.rfile)
        if (acknowledgement.type != 'ack'):
            print 'client sent message but acknowledgement NOT received', acknowledgement
        #print 'client sent message and acknowledgement received'
        #print task_to_server

    #put error methods here
    def receive(self):
        try:
            from_server = load(self.rfile)
        except socket.timeout as e:
            print 'socket timeout: %s' % e
            return False
        except EOFError as e:
            print 'no pickle sent to load: %s' % e
            return False
        else:
            self.acknowledge()
            #print 'client received message and sent acknowledgement'
            #print from_server
            return from_server

        #send back to acknowledge request received
    def acknowledge(self):
        acknowledgement = message.Message("ack", ['time_sent_ack', 'time_rec_message'])
        dump(acknowledgement, self.wfile, 2)
        #self.logger.info('acknowledge pickled and sent: %s %s' % acknowledgement)

    def login(self):

        while True:
            username = raw_input(Logon_Client.login_prompt[0])
            password = raw_input(Logon_Client.login_prompt[1])

            self.send(message.Message('login', [username, password]))


            response = self.receive()
            if (response.data[0] == 's'):
                print 'login success: %s' % response
                self._handle()
            elif (response.data[0] == 'u'):
                print 'wrong username: %s' % response
            elif (response.data[0] == 'p'):
                print 'wrong password: %s' % response
            else:
                print 'login failed'
                print response
                return False


    def _handle(self):



        while True:
            command = raw_input('Enter command(update, toggle, timed_on, end): ')
            if command == 'update':
                data = ['update info']
            elif command == 'toggle':
                data = [int(raw_input('select motorid 0 through 7: '))]
            elif command == 'timed_on':
                motor = int(raw_input('select motorid 0 through 7: '))
                time = int(raw_input('enter time amount in seconds: '))
                data = [motor, time]
            elif command == 'end':
                return
            else:
                print 'did not recognized command'
                continue
            self.send(message.Message(command, data))
            response = self.receive()
            if (response.type == 'end'):
                return


if __name__ == '__main__':
    client = Logon_Client()
    client.login()










