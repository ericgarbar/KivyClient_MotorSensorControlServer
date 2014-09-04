__author__ = 'Eric'

import threading
import Queue
import time
import mediator as module_med
#testing modulator import version of mediator, why mediator is
#commented out, not sure if necessary if name is overridden??
class task(object):
    def __init__(self, data, command = None, response = None, signal = None):
        self.type = command
        self.command = command
        self.data =data
        self.response = response
        self.signal = signal

    def __str__(self):
        print self.command



'''class mediator(object):
    def __init__(self, control):
        self.control = control
        self.task_queue = Queue.Queue()
        t = threading.Thread(target=self.serve)
        t.setDaemon(True)
        t.start()

    def serve(self):
        while True:
            #get task object
            user_task = self.task_queue.get()
            print user_task
            user_task.response = self.control.do_task(user_task)
            user_task.signal.set()

    def relay_task(self, task):
        self.task_queue.put(task)'''

class user(object):
    relayer = None
    def __init__(self):
        pass


    def turn_on(self, data):
        user_task = task(command='on', data=data)
        response = user.relayer.relay_task(user_task)

        print 'response is: ', response

    def turn_off(self, data):

        user_task = task(command='off', data=data)
        response = user.relayer.relay_task(user_task)
        print 'response is: ', response

    @staticmethod
    def add_relayer(mediator):
        user.relayer = mediator

#motor control simulator, instance will be accessed by multiple threads
#uses queue to moderate access, threads still don't get served in exact order,
#since the socket communication part of each thread is still unpredictable,
#order doesn't matter so much as each request getting served promptly and
#reliably
class controller(object):

    def __init__(self):
        self.my_motors = ['off' for i in range(20)]

    def do_task(self, task):
        if task.command=='on':
            self.my_motors[task.data] = 'on'
            return 'turned motor%d on' % task.data
        elif task.command == 'off':
            self.my_motors[task.data] = 'off'
            return 'turned motor%d off' % task.data
        else:
            print 'unrecognized command'

    def turn_on(self, data):
        self.my_motors[data] = 'on'
        return 'motor%d: turned on' % data

    def turn_off(self, data):
        self.my_motors[data] = 'off'
        return 'motor%d: turned off' % data

    def toggle_state(self, data):
        if self.my_motors[data] == 'on':
            self.my_motors[data] = 'off'
        else: self.my_motors[data] == 'on'

    def update(self):
        pass

    def __str__(self):
        return str(self.my_motors)
#first initialize control
control = controller()
print 'control made'
#pass control to thread mediator instance in order to moderate access
med = module_med.mediator(control)
print 'mediator made'
#add mediator for entire user class as static method
#concious decision since all user instances need a
#way of relaying requests to execute a request for
#action on the server
user.add_relayer(med)
'mediator added to user class'

#create a bunch of a threads to test mediator
for i in range(20):
    client = user()
    t = threading.Thread(target=client.turn_on, args=(i,))
    t.daemon = True
    t.start()

#give time to sleep so that all get turned on
#want to change to join or wait for all threads to end
#and would be cool to time it as well
time.sleep(2)
print 'controller', control








