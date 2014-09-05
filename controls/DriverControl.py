__author__ = 'Eric'
from drivers.Driver import Driver

class DriverControl(object):

    #initialize drivers and pass as a list
    #assumed that index will be passed to identify driver to control
    def __init__(self, drivers=None, max_drivers_on=None, **kwargs):

        #implement error checking for no drivers
        self.total_drivers_on = 0
        self.max_drivers_on = max_drivers_on
        self.haslimit = False
        if self.max_drivers_on is not None: self.haslimit = True
        self.at_limit = False
        self.drivers = drivers
        self.total_drivers = len(drivers)
        for driver in drivers:
            driver.control = self



    def __str__(self):
        #put names of drivers in list, then join into one long string concatenated string
        return "\n".join([d.get_information() for d in self.drivers])

    def update(self):
        return self.__str__()


    #toggle_state checks state of passed driverid and then hands off to appropriate turn_on, turn_off method
    #and returns new state, bookkeeping is done in turn_off, turn_on including checking if at max drivers
    def toggle_state(self, driverid):
        if self.drivers[driverid].state == 'On':
            print "enter toggle off"
            self.turn_off(driverid)
            print self.update()
            return self.update()
        else:
            if self.turn_on(driverid):
                print "enter toggle on"
                self.turn_on(driverid)
                print self.update()
                return self.update()
            else: return 'Off'

    def turn_on(self, driverid):
        if self.drivers[driverid].state == 'On': return (False, 'Driver already on!')
        else: #driver off
            if self.haslimit:#check if at limit
                if self.total_drivers_on < self.max_drivers_on:
                    print "entered totaldrivers < max"
                    self.drivers[driverid].turn_on()
                    self.total_drivers_on += 1
                    return True
                else:#return false if driver remains off due to limit
                    return False

            else:
                self.drivers[driverid].turn_on()
                return True

    def turn_off(self, driverid):
        if self.drivers[driverid].state == 'Off': return 'Driver already off!'
        else:
            self.drivers[driverid].state = 'Off'
            self.total_drivers_on -= 1
            return True





if __name__=='__main__':
    drivers = [Driver.Driver(chip=None) for i in range (0, 8)]
    driver_control = DriverControl(drivers=drivers, max_drivers_on=3)
    print "max drivers on is %d" % driver_control.max_drivers_on

    print driver_control.turn_on(0)
    print driver_control.drivers[0].state
    print driver_control.turn_off(0)
    print driver_control.drivers[0].state
    print driver_control.turn_on(0)
    print driver_control.drivers[0].state





