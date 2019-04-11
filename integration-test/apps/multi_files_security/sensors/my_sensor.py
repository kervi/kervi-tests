""" Module for a sensor """
from kervi.sensors import Sensor
from kervi.devices.sensors.dummy_sensor import DummySensorDeviceDriver

class MySensor(Sensor):
    """ My sensor """
    def __init__(self):
        Sensor.__init__(self, "mySensor", "My sensor", DummySensorDeviceDriver())
        self.type = "temp"
        self.max = 100
        self.min = 0
        self.unit = "C"

        #self.link_to_dashboard("app", "sensors", type="radial_gauge")

MySensor()
 
