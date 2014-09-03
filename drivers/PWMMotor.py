from drivers import Driver

__author__ = 'Eric'


class PWMMotor(Driver):

    def __init__(self, **kwargs):
        super(PWMMotor, self).__init(**kwargs)
        self.freq = 0 #Hz, number of cycles per second
        self.dutycycle = 0 #percent of dutycycle active