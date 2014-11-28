__author__ = 'Eric'

import Queue
import threading
import message
import time




class mediator(object):


    def __init__(self, control):
        self.control = control
        self.task_queue = Queue.PriorityQueue()
        self.stay_alive = threading.Event()
        self.stay_alive.set()

        t = threading.Thread(target=self._run)
        t.setDaemon(True)
        t.start()

        #will vary from control to control
        self.TEST_PRIORITIES = {
            'on': 0,
            'off':0,
            'toggle':0,
            'name': 0,
            'update':1,
            'timed_on':0,
            'timer': 0
        }

        self.CONTROL_COMMANDS = {
            'on' : self.control.turn_on,
            'off' : self.control.turn_off,
            'toggle': self.control.toggle_state,
            'update': self.control.update,
            'name': self.control.change_name,
            'timer': self.control.set_timer
        }



    #maybe need to do lock and release for access the class mediator, worked ok in test
    #of twenty users, just with threads not in predictable chronological order
    #user_task is passed as message with fields type(str), data([])
    def process_request(self, user_task):
        #signal is triggered upon completion of task
        signal = threading.Event()
        #put in task queue
        self.task_queue.put((self.TEST_PRIORITIES[user_task.type], (user_task, signal)))
        #once signal is triggered from run thread where task_queue is controlled
        #there will be a user_task response object,
        # initialize response as none for task type and then changed in run() thread

        if (signal.wait(5)):
            return user_task.response
        print 'task timed out'



    def _run(self):
        while(self.stay_alive.is_set()):
            #has to timeout in order to still check while condition even if queue is empty,
            #set timeout and block instead of not block so that it is not constantly cycling as well
            try:
                user_task, signal = self.task_queue.get(True, 0.1)[1]
                print 'from queue', user_task
            except Queue.Empty as e:
                #should set to be woken up by queue when it is not empty
                #then continue
                time.sleep(0.1)
                continue
            user_task.response = self.CONTROL_COMMANDS[user_task.type](*user_task.data)
            signal.set()


    '''class task_process_timeout(Exception):

        print 'task process of %s timeout after: %d seconds' % (5, )
        WILL WORK ON EXCEPTIONS LATER'''
