__author__ = 'Eric'

import SocketServer
import threading
import collections
import cPickle
import time
import logging
import socket
import thread
import select
import message
import Queue
import mediator
from controls import DriverControl
from drivers import Driver


SERVER_ADDRESS = ('localhost', 9000)
TIMEOUT = 120
UPDATE_PRIORITY = 1
REQUEST_PRIORITY = 0

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
    def add_mediator(self, mediator):
        MyRequestHandler.mediator = mediator


    def handle(self):

        #create logger with client_address prop of socket/request which is initialized in __init__
        # if login is successful will change logger name to the user who logged in
        self.logger = logging.getLogger(str(self.client_address))

        #setting timeout on socket, so that if readline is called and no information is received in 3 seconds then
        #error is raised

        #users is dictionary of allowable user names and corresponding passwords
        #probably should go somewhere else eventually, encrypted file or something...
        self.users = {'gardener':'', 'gardener2':'gardengarden'}

        MyRequestHandler.total_clients += 1
        #communication loop

        acknowledge = message.Message('ack', ['time received request', 'time sent response'])
        self.send(acknowledge)
        self.logger.info('acknowledge pickled and sent: %s' % acknowledge)

        #returns false if too many incorrect password tries, login timesout, or socket read times out
        #handles error logging in method
        #return goes back to __init__ call where finish is then called to clean up socket, files, etc
        #will log successful login as well, changes and returns socket.settimeout() to original value
        #sends
        if not self.check_password():
            self.logger.info('incorrect login closing connection')
            return


        #receive can throw timeout error
        client_request = self.receive()
        self.logger.info('received %s request' % client_request.type)

        self.send()
        while True:


            self.relay_request(client_request)

            client_request = self.receive()
            print "received %s request" % client_request
            self.send()


    def status_request(self, data):
        return message.Message('Status', ['status of data'])
    def toggle_request(self, data):
        return message.Message('reject/accept', ['new status'])
    def timer_request(self, data):
        return message.Message('reject/accept', ['new status'])
    def schedule_request(self, data):
        return message.Message('reject/accept', ['new status'])
    def end_request(self, data):
        return message.Message('end', ['closing connection'])

    def relay_request(self, client_request):
        #might change to different object for mediator to process
        mediator.process(client_request)








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
            self.logger.info('login attempts %d' % attempts)
            try:
                #load automatically reads exactly one pickle from file and unloads it back into object form
                request =  self.receive()
                self.logger.info('message loaded and unPickled: %s' % request)

            #need to print tracebacks for errors in log, and catch all network/unpickling errors
            except EOFError as e:
                self.logger.error('eof error: %s' % request)
                return False
            except ImportError as e:
                self.logger.error('import error', time.time(), )
                return False
            #timeout will return false for check_password if timeout error occurs, which then causes handle method
            # to return to server.finish_request for MyRequestHandler.finish() request to be called and socket closed
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
                    self.logger.name = user_data[0]
                    self.request.settimeout(TIMEOUT)
                    self.send(message.Message('accept', ['s']))
                    return True
                elif (login_attempt == 'u'):
                    self.logger.info('incorrect username: ' + user_data[0])
                    response = message.Message('reject',['u'])
                    self.send(response)
                    self.logger.info('pickled and sent response: %s' % response)
                elif (login_attempt == 'p'):
                    self.logger.info('incorrect password with user: ' + user_data[0])
                    self.send(message.Message('reject',['p']))
        self.logger.info('login failed')
        self.send(message.Message('close', ['login fail']))
        self.request.settimeout(TIMEOUT)
        return False

    def finish(self):
        SocketServer.StreamRequestHandler.finish(self)
        MyRequestHandler.total_clients -= 1

    #send to_client parameter client pickling and then dumping into self.wfile
    def send(self, to_client=message.Message(['ack', ['timesent']])):
        cPickle.dump(to_client, self.wfile, 2)

    def receive(self):
        try:
            return cPickle.load(self.rfile)
        except EOFError as e:
            self.logger.error('no pickle sent to load: %s' % e)


class MyServer(SocketServer.ThreadingTCPServer):

    def __init__(self, server_address, request_handler):
        SocketServer.ThreadingTCPServer.__init__(self, server_address, request_handler)

        
'''using modular import for mediator class instead
class Mediator(object):

    def __init__(self, call_object):
        self.queue = Queue.Queue()
        self.caller

    def process(self, task):
        self.queue.put(task)

    def _do_tasks(self):
        while True:
            task = self.queue.get(True)
            self.caller.task.action(*task.args)
'''

class Fake_Motor_Control(object):
    pass



drivers = [Driver.Driver(chip=None, channel=i) for i in range(0,8)]
motor_control = DriverControl.DriverControl(drivers=drivers)
mediator = mediator.Mediator(motor_control)
MyRequestHandler.add_mediator(mediator)

Rpi_Server = MyServer(SERVER_ADDRESS, MyRequestHandler)
threading.Thread(target=Rpi_Server.serve_forever).start()










