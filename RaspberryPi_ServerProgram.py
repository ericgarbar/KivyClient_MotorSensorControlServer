__author__ = 'Eric'

import logging
import threading

from controls import DriverControl
from drivers.Driver import Driver
from controls.DriverControl import DriverControl
from server_rpi.Server_RPi import Server_RPi



SERVER_ADDRESS_ONE = ('localhost', 9000)
SERVER_ADDRESS_TWO = ('localhost', 9001)


logging.basicConfig(level=logging.DEBUG,
                    format='%(name)s: %(message)s',
                    )

drivers = [Driver(chip=None, channel=i) for i in range(0,8)]
motor_control = DriverControl(drivers=drivers, name='this control')

this_RPi_Server = Server_RPi(SERVER_ADDRESS_ONE, motor_control)
threading.Thread(target=this_RPi_Server.serve_forever).start()

drivers = [Driver(chip=None, channel=i) for i in range(0,8)]
motor_control = DriverControl(drivers=drivers, name='that control')

that_RPi_Server = Server_RPi(SERVER_ADDRESS_TWO, motor_control)
threading.Thread(target=that_RPi_Server.serve_forever).start()

