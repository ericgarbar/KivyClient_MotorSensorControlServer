__author__ = 'Eric'
from time import time, sleep

class Track_Timer(object):

    def __init__(self, start_time=None, duration=None, driverid=None, timer_thread=None):
        self.driverid = driverid #driverid for control to send to client
        self.start_time = start_time
        self.duration = duration
        self.timer_thread = timer_thread
        self.timer_thread.start()

    @property
    def remaining_time(self):
        remaining = self.duration - ((time()) - self.start_time)
        hours = int(remaining / 3600)
        minutes = int((remaining % 3600) / 60)
        seconds = int(remaining % 60)
        return "{0:02d}:{1:02d}:{2:02d}".format(hours, minutes, seconds)

    def cancel(self):
        self.timer_thread.cancel()


if __name__ == '__main__':
        timer_test = Track_Timer(time(), 3663)
        print timer_test.remaining_time
        for i in range(10):
            sleep(1)
            print timer_test.remaining_time