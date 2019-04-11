    
from kervi.dashboards import Dashboard, DashboardPanel
    
#Define dashboards and panels
Dashboard(
    "layout",
    "Layout",
    [
        DashboardPanel("fan", title="CPU fan", width=50),
        DashboardPanel("p1", title="Panel 2", width=25),
        DashboardPanel("p2", title="Panel 3", width=25)
    ],
    is_default=False
)

#create sensor
from kervi.sensors import Sensor
from kervi.devices.sensors.system import CPULoadSensorDeviceDriver
from kervi.devices.sensors.system import CPUTempSensorDeviceDriver
from kervi.devices.sensors.dummy_sensor import DummySensorDeviceDriver
#create a senors that uses CPU load device driver
cpu_load_sensor = Sensor("CPULoadSensor","CPU", CPULoadSensorDeviceDriver())

#link to dashboard
cpu_load_sensor.link_to_dashboard("*", "header_right", show_sparkline=True)
cpu_load_sensor.link_to_dashboard("layout", "p1", type = "value", show_sparkline=True, link_to_header=True)
cpu_load_sensor.link_to_dashboard("layout", "p1", type="chart")
cpu_load_sensor.link_to_dashboard("layout", "p2", type="chart")
#create a senors that uses CPU temp device driver
cpu_temp_sensor = Sensor("CPUTempSensor","CPU temp", DummySensorDeviceDriver())

#link to dashboard
cpu_temp_sensor.link_to_dashboard("layout", "p2", type="radial_gauge")

#define a controller
from kervi.controllers import Controller
from kervi.values import NumberValue

class FanController(Controller):
    def __init__(self):
        Controller.__init__(self, "fan_controller", "Fan")

        #define an input that is a number
        self.temp = self.inputs.add("temp", "Temperature", NumberValue)
        self.temp.min = 0
        self.temp.max = 150
        
        #define an output that is a number
        self.fan_speed = self.outputs.add("fan_speed", "Fan speed", NumberValue)

    #input_changed is called by the framework when any of the controller inputs changes its value.
    def input_changed(self, changed_input):
        temp = self.temp.value
        if temp <= 20:
            self.fan_speed.value = 0
        else:
            speed = (temp / 80) * 100
            if speed > 100:
                speed = 100
            self.fan_speed.value = speed

#Instantiate the controller
fan_controller = FanController()

#show the controller input and output in the ui.
fan_controller.temp.link_to_dashboard("layout", "fan")
fan_controller.fan_speed.link_to_dashboard("layout", "fan")

#link the fan controllers temp input to cpu temperature sensor
fan_controller.temp.link_to(cpu_temp_sensor)

#link to the motor controller device
#from kervi.devices.motors.adafruit_i2c_motor_hat import AdafruitMotorHAT
#motor_driver = AdafruitMotorHAT()
#motor_driver.dc_motors[0].speed.link_to(fan_controller.fan_speed)
