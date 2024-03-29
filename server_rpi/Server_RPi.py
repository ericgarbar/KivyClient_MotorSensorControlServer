from server_rpi import mediator

__author__ = 'Eric'

import SocketServer
import cPickle
import time
import logging
import socket
import message


TIMEOUT = 120
logging.basicConfig(level=logging.DEBUG,
                format='%(name)s: %(message)s',
                    )



class MyRequestHandler(SocketServer.StreamRequestHandler):

    #keep track of how many clients currently logged on
    total_clients = 0
    #def setup(): sets up self.rfile for reading and self.wfile for writing)
    #buffer for rfile is default of 8192, wfile is 0 or unbuffered so DON'T NEED TO USE FLUSH as normally would
    #with files

    @staticmethod
    def add_mediator(mediator):
        MyRequestHandler.my_mediator = mediator

    #send to_client parameter client pickling and then dumping into self.wfile
    def send(self, type, data):
        to_client_message = message.Message(type, data)
        cPickle.dump(to_client_message, self.wfile, 2)

        client_ack = cPickle.load(self.rfile)
        if (client_ack.type != 'ack'):
            self.logger.debug('message sent to client but acknowledgement not received')
        self.logger.debug('message sent to client and acknowledgement received')


    #returns unpickled object from socket connection
    #will be a request from client as message object
    #message has two fields type and data
    def receive(self):
        try:
            user_request = cPickle.load(self.rfile)
        except EOFError as e:
            self.logger.error('no pickle sent to load: %s' % e)
        else:
            self.acknowledge()
            self.logger.debug('server received user request and client sent acknowledgement')
            self.logger.debug(user_request)
            return user_request

    #send back to acknowledge request received
    def acknowledge(self):
        acknowledgement = message.Message("ack", ['time_sent_ack', 'time_rec_message'])
        cPickle.dump(acknowledgement, self.wfile, 2)

    def relay_request(self, client_request):
        #might change to different object for mediator to process
        return ('motor_response', MyRequestHandler.my_mediator.process_request(client_request))

    def handle(self):

        #create logger with client_address prop of socket/request which is initialized in __init__
        # if login is successful will change logger name to the user who logged in
        self.logger = logging.getLogger(str(self.client_address))

        #users is dictionary of allowable user names and corresponding passwords
        #probably should go somewhere else eventually, encrypted file or something...
        self.users = {'gardener':'', '':'', 'gardener2':'gardengarden'}

        MyRequestHandler.total_clients += 1 #increase to reflect new number of users logged in


        self.acknowledge() #send acknowledge ment to know connection successful
        self.logger.debug('acknowledge successful connection')

        if not self.check_password():
            self.logger.error('incorrect login closing connection')
            self.finish()
            return #return goes back to __init__ call where finish is then called to clean up socket, files, etc


        #receive can throw timeout error and handle timeout error, will call finish and return
        client_request = self.receive()
        assert client_request!=None
        while client_request.type != "end":
            response = self.relay_request(client_request) #returns tuple for values to send
            self.send(*response)
            client_request = self.receive()


    #checks user password parameters against self.user dict, where user = key, password = value
    #returns s for succes, u for incorrect user, p for incorrect password
    def check_user(self, user, password):
        #possibly more type checks before evaluating password to compare
        #possible to maybe unpickle and execute sent malicious code at this point
        try:
            if (password == self.users[user]):
                return 's'

        except KeyError as e:
            return 'u'
        else:
            return 'p'

    #will log successful login as well, changes and returns socket.settimeout() to original value
    #sends
    def check_password(self):

        #client will send info such that user_data[0] = "username", user_data[1] = "password"
        #call check_user to look up password of username in users dictionary and compare it
        #to provided password while loop checks to see if 120 seconds is up and then connection will terminate or login
        #attempts

        self.logger.info('now checking password')
        attempts = 0
        starttime = time.time()
        #can wait 1 minute for user to try to login between password attempts
        self.request.settimeout(60)

        while(attempts < 10 and time.time()-starttime < 180):
            attempts += 1
            self.logger.info('login attempt %d' % attempts)
            try:
                request =  self.receive() #request type is 'login', data = [username, password]
                self.logger.info('request loaded and unPickled: %s' % request)

            #need to print tracebacks for errors in log, and catch all network/unpickling errors
            #timeout will return false for check_password if timeout error occurs, which then causes handle method
            #to return to server.finish_request for MyRequestHandler.finish() request to be called and socket closed
            except EOFError as e:
                self.logger.error('eof error: %s' % request)
                return False
            except ImportError as e:
                self.logger.error('import error', time.time(), )
                return False
            except socket.timeout as timeout:
                self.logger.info('timeout by: %s %s' % self.client_address)
                return False
            else:
                #client will send info such that user_data[0] = "username", user_data[1] = "password"
                user_data = request.data
                login_attempt = self.check_user(*user_data)
                if (login_attempt == 's'):
                    self.logger.info('login successful for user: ' + user_data[0])
                    self.logger.info('change logger name to: ' + user_data[0])
                    self.logger.info('resetting socket timeout to default')
                    self.logger.name = user_data[0]
                    self.request.settimeout(TIMEOUT)
                    self.send('accept', ['s'])
                    return True
                elif (login_attempt == 'u'):
                    self.logger.info('incorrect username: ' + user_data[0])
                    self.send('reject', ['u'])
                    self.logger.info('pickled and sent response rejection response')
                elif (login_attempt == 'p'):
                    self.logger.info('incorrect password with user: ' + user_data[0])
                    self.send('reject', ['p'])
        self.logger.info('login failed')
        self.send(message.Message('close', ['login fail']))
        self.request.settimeout(TIMEOUT)
        return False

    def finish(self):
        MyRequestHandler.total_clients -= 1
        SocketServer.StreamRequestHandler.finish(self)





class Server_RPi(SocketServer.ThreadingTCPServer):

    def __init__(self, server_address, motorcontrol):
        self.my_mediator = mediator.mediator(motorcontrol)
        MyRequestHandler.add_mediator(self.my_mediator)
        SocketServer.ThreadingTCPServer.__init__(self, server_address, MyRequestHandler)





if __name__ == '__main__':
    SERVER_ADDRESS_ONE = ('localhost', 9000)
    import threading
    from drivers.Driver import Driver
    from controls.DriverControl import DriverControl

    drivers = [Driver(chip=None, channel=i) for i in range(0,8)]
    motor_control = DriverControl(drivers=drivers, name='this control')

    this_RPi_Server = Server_RPi(SERVER_ADDRESS_ONE, motor_control)
    threading.Thread(target=this_RPi_Server.serve_forever).start()








