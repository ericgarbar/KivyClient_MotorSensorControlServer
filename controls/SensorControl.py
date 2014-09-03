__author__ = 'Eric'

from sensors.Sensor import Sensor

class SensorControl(object):

    def __init__(self, sensors=None):
        self.sensors = sensors
        self.water_sensors = []
        self.light_sensors = []
        self.hum_sensors = []
        self.temp_sensors = []
        for sensor in self.sensors:
            if sensor.type == 'Water': self.water_sensors.append(sensor)
            elif sensor.type == 'Light': self.light_sensors.append(sensor)
            elif sensor.type == 'Temperature': self.temp_sensors.append(sensor)
            elif sensor.type == 'Humidity':  self.hum_sensors.append(sensor)


    def get_water_reading(self):
        return [(sensor.name, sensor.get_reading(), sensor.unit) for sensor in self.water_sensors]

    def get_light_reading(self):
        return [(sensor.name, sensor.get_reading(), sensor.unit) for sensor in self.light_sensors]

    def get_humidity_reading(self):
        return [(sensor.name, sensor.get_reading(), sensor.unit) for sensor in self.hum_sensors]

    def get_temperature_reading(self):
        return [(sensor.name, sensor.get_reading(), sensor.unit) for sensor in self.temperature_sensors]



