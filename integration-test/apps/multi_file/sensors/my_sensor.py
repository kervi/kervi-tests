""" Module for a sensor """
from kervi.sensors import Sensor
from kervi.devices.sensors.dummy_sensor import DummySensorDeviceDriver, DummyMultiDimSensorDeviceDriver

class MySensor(Sensor):
    """ My sensor """
    def __init__(self):
        Sensor.__init__(self, "mySensor", "My sensor x", DummySensorDeviceDriver(unit="c"))
        self.value_type = "temperature"
        self.add_error_range((0, 10), "l error message", channels=["user_log", "email"])
        self.add_warning_range((10, 20), "l warning message")
        self.add_normal_range((20, 80), "normal", channels=["user_log", "email"])
        self.add_warning_range((80, 90), "h warning message",channels=["user_log", "email"])
        self.add_error_range((90, 100), "h error message", channels=["user_log", "email"])

        self.link_to_dashboard("app", "sensors", type="radial_gauge")
        self.link_to_dashboard("app", "sensors", type="value", show_sparkline=True)


MySensor()

BATTERY_SENSOR = Sensor("Battery","Battery", DummySensorDeviceDriver())
BATTERY_SENSOR.set_ui_parameter("value_icon", [
    {
        "range":[0, 5],
        "icon":"battery-empty"
    },
    {
        "range":[5, 25],
        "icon":"battery-quarter"
    },
    {
        "range":[20, 50],
        "icon":"battery-half"
    },
    {
        "range":[5, 75],
        "icon":"battery-three-quarters"
    },
    {
        "range":[75, 100],
        "icon":"battery-full"
    }
])
BATTERY_SENSOR.link_to_dashboard(link_to_header=True, display_unit=False, show_sparkline=False, show_value=False)



MULTI_SENSOR = Sensor("MultiSensor","Multi dimension", DummyMultiDimSensorDeviceDriver())
MULTI_SENSOR.link_to_dashboard(panel_id="sensors", type="value")
MULTI_SENSOR.link_to_dashboard()