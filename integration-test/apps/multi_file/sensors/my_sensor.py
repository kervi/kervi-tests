""" Module for a sensor """
from kervi.sensors.sensor import Sensor
from kervi.devices.sensors.dummy_sensor import DummySensorDeviceDriver

class MySensor(Sensor):
    """ My sensor """
    def __init__(self):
        Sensor.__init__(self, "mySensor", "My sensor", DummySensorDeviceDriver())
        self.value_type = "temperature"
        self.add_error_range((0, 10), "l error message", channels=["user_log", "email"])
        self.add_warning_range((10, 20), "l warning message")
        self.add_warning_range((80, 90), "h warning message")
        self.add_error_range((90, 100), "h error message", channels=["user_log", "email"])

        self.link_to_dashboard("app", "sensors", type="radial_gauge")

MySensor()
 
