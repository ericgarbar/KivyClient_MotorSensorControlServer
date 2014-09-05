__author__ = 'Eric'
import time



class Driver(object):
    id = 0
    def __init__(self, chip=None, name='Driver', channel=None, time_limit=False, **kwargs):

        #chip will provide interface to the hardware so driver can turn itself off and on in physical world
        self.chip = chip
        self.channel = channel

        #initialize state to off
        self.state = "Off"
        self.state_timer = time.time()
        #time limit caps amount of time driver can be in certain state
        self.time_limit = time_limit
        if time_limit:
            self.max_time = 


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

    def is_driver(self):
        return True

    def is_sensor(self):
        return False

    def is_on(self):
        return self.state == "On"

    def get_information(self):
        return "{driver} on {chip} channel {channel} is {state}".\
            format(driver = self.name, chip = 'chip', channel = self.channel, state=self.state)

    def turn_on(self): #note and is logical AND, where & is bitwise AND
        if ((self.chip is not None) and (self.channel is not None)): self.chip.on(self.channel)
        self.state = "On"
        self.begin_state_time = time.time()
        if self.time_limit:
            time.sleep(self.time_limit)
            self.turn_off()

    def turn_off(self):
        if ((self.chip is not None) and (self.channel is not None)): self.chip.off(self.channel)
        self.state = "Off"
        self.begin_state = time.time()

    def set_control(self, drivercontrol):
        self.control = drivercontrol

    def __str__(self):
        return str(self.state)

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