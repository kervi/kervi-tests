if __name__ == '__main__':

    from kervi.application import Application
    
    app = Application()

    from kervi.dashboards import Dashboard, DashboardPanel
    Dashboard(
        "app",
        "My application",
        [
            DashboardPanel("cpu"),
            DashboardPanel("fan_temp", width=25),
            DashboardPanel("fan_speed")
        ],
        is_default=True #This is the default dashboard that is shown when the ui loads.
    )


    #create sensors
    from kervi.sensors import Sensor
    from kervi.devices.sensors.system import CPUTempSensorDeviceDriver
    from kervi.devices.sensors.dummy_sensor import DummySensorDeviceDriver
    #create a senors that uses CPU temp device driver
    cpu_temp_sensor = Sensor("CPUTempSensor","CPU temp", DummySensorDeviceDriver())
    
    #link to dashboard
    cpu_temp_sensor.link_to_dashboard("app", "cpu", type = "value", show_sparkline=True, link_to_header=True)
    cpu_temp_sensor.link_to_dashboard("app", "cpu", type="chart")

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
    fan_controller.temp.link_to_dashboard("app", "fan_temp")
    fan_controller.fan_speed.link_to_dashboard("app", "fan_speed")

    #link the fan controllers temp input to cpu temperature sensor
    fan_controller.temp.link_to(cpu_temp_sensor._sensor_value)
    
    #link to the motor controller device
    #from kervi.devices.motors.adafruit_i2c_motor_hat import AdafruitMotorHAT
    #motor_driver = AdafruitMotorHAT()
    #motor_driver.dc_motors[0].speed.link_to(fan_controller.speed)

    app.run()