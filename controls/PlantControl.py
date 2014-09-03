__author__ = 'Eric'

from DriverControl import DriverControl
from SensorControl import SensorControl
from kivy.clock import Clock
import time

class PlantControl(object):

    def __init__(self, sensorcontrol=None, drivercontrol=None, name=None, *args, **kwargs):

        pass



class Scheduler(object):

    def __init__(self, time_on=None, calling_obj_on=None, time_off=None, calling_obj_off=None):
        #time_on, time_off are strings, will convert to seconds from epoch then compare to current time from epoch
        #then schedule in future using kivy's clock.schedule_once

        #time on has to be of format 'Fri Jun 06 09:44:16 2014', abbreviated day, abbreviated month, day, HH:MM:SS, year
        #construst
        self.time_on = time.strptime(time_on, '%a %b %d %H:%M:%S %Y')
        self.time_off = time.strptime(time_off, '%a %b %d %H:%M:%S %Y')

        #convert to since epoch time
        self.time_on = time.mktime(self.time_on)
        self.time_off = time.mktime(self.time_off)

        #compare to current time to schedule
        current_time = time.time()
        time_til_on = self.time_on - current_time
        time_til_off = self.time_off - current_time
        Clock.schedule_once(calling_obj_on, time_til_on)
        Clock.schedule_once(calling_obj_off, time_til_off)

    def schedule_begin_end_tasks(self):
        pass

    def schedule_threshold(self):
        pass









class Threshold(object):

    def __init__(self, boundary=None, below=True, incident_limit=1, trigger=None, get_data=None, trigger_limit=0):
        self.boundary = boundary #value passed in to be monitored
        self.below = below #watch for value going below boundary, False if for watching above
        self.incidents = 0
        self.incident_limit = incident_limit #numbers of times boundary passed before trigger called
        self.trigger = trigger #calling object.function to trigger when boundary crossed and incident limit reached
        self.get_data = get_data #calling object.function to call to get current value to check against boundary
        self.total_triggers = 0
        self.trigger_limit = trigger_limit


    def check_boundary(self):
        if self.below: #check if current value is lower than boundary
            if self.get_data() < self.boundary:
                self.incidents += 1
                if self.incidents == self.incident_limit:
                    self.trigger() #call trigger if data source has crossed below boundary
                    self.total_triggers += 1
                    self.incidents = 0
        else:
            if self.get_data() > self.boundary:
                self.incidents += 1
                if self.incidents == self.incident_limit:
                    self.trigger() #call trigger if data source has crossed above boundary
                    self.total_triggers += 1
                    self.incidents = 0





if __name__ == '__main__':
    print 'main'