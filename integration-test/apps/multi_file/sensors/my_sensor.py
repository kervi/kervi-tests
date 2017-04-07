""" Module for a sensor """
from kervi.sensor import Sensor
from kervi_devices.sensors.dummy_sensor import DummySensorDeviceDriver



class MySensor(Sensor):
    """ My sensor """
    def __init__(self):
        Sensor.__init__(self, "mySensor", "My sensor", DummySensorDeviceDriver())
        self.type = "temp"
        self.max = 100
        self.min = 0
        self.unit = "C"

        self.upper_fatal_limit = 80
        self.upper_fatal_message = "Upper fatal"

        self.upper_warning_limit = 70
        self.upper_warning_message = "Upper warning"

        self.lower_fatal_limit = 20
        self.lower_fatal_message = "lower fatal"

        #self.lower_warning_limit =30
        #self.lower_warning_message = "lower warning"

        self.normal_message = "normal message"

        #link the sensor to a dashboard section
        self.link_to_dashboard("app", "sensors", type="radial_gauge")

MySensor()
 
