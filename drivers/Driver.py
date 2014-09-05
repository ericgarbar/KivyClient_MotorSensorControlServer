__author__ = 'Eric'
import time



class Driver(object):
    id = 0
    def __init__(self, chip=None, name='Driver', channel=None, time_limit=False, **kwargs):

        #chip will provide interface to the hardware so driver can turn itself off and on in physical world
        self.chip = chip
        self.channel = channel
        if chip is None and type is None:
            self._abstract = True
        else:
            self._abstract = False


        #initialize state to off
        self.state = "Off"
        self.get_get_state_timer = time.time()
        #time limit caps amount of time driver can be in certain state
        self.time_limit = time_limit
        #max_time_limit is in seconds in order to ocmpare to time.time easily
        if time_limit:
            self.max_time = 0 #limit must still be set, evals to false when checking on method
        else:
            self.max_time = -1 #evaluates to True, unlimited with no time_limit, declare still for future limit changes


        #rename to include current id #, can't pass as optional keyword since those values are binded
        #at time of class creation so the optional paramter would always be binded to 0

        self.name = name
        if self.name == 'Driver': self.name += '%d' % Driver.id
        self.id = Driver.id
        Driver.id += 1

        #control attribute can point to driver controller
        self.control = None



    def get_state(self):
        return self.state

    def is_on(self):
        return self.state == "On"

    def is_off(self):
        return self.state == 'Off'

    def get_state_time(self):
        #get difference in times between now and when state was entered
        seconds = time.time() - self.state_start_time
        #convert raw data into hour:minutes:seconds time struct
        minutes = seconds/60
        seconds = seconds % 60
        hours = minutes / 60
        minutes = minutes % 60
        return (hours, minutes, seconds)
    
    def p_state_time(self):
        "hrs:{hours}min:{mins}sec:{sec}".format(*self.get_state_time())

    def set_time_limit(self, minutes=0, hours=0, seconds=0):
        max_time_limit = minutes * 60 + hours * 3600 + seconds


    def turn_on(self): #note and is logical AND, where & is bitwise AND
        if ((self.chip is not None) and (self.channel is not None)): self.chip.on(self.channel)
        self.state = "On"
        self.state_start_time = time.time()
        if self.time_limit:
            time.sleep(self.time_limit)
            self.turn_off()

    def turn_off(self):
        if ((self.chip is not None) and (self.channel is not None)): self.chip.off(self.channel)
        self.state = "Off"
        self.state_start_time = time.time()

    def set_control(self, control):
        self.control = control

    def __str__(self):
        if self._abstract:
            return "{driver} is {state} for {time}".format\
                (driver=self.name, state=self.state, time=self.get_state_time())
        else:
            return "{driver} on {chip} channel {channel} is {state}".\
            format(driver = self.name, chip = 'chip', channel = self.channel, state=self.state)

if __name__=='__main__':
    driver = Driver()
    print driver.state
    driver.turn_on()
    print "turned driver on, driver state is", driver.state
    driver.turn_off()
    print "turned driver off, driver state is", driver.state
    driver.turn_on()
    print "turned back on, driver state should be on. driver state is: ", driver.state
    print time.time()
    print time.time()
    print driver.name

    print Driver().name