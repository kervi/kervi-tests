if __name__ == '__main__':
    from kervi.application import Application
    APP = Application()
    
    from kervi.dashboards import Dashboard, DashboardPanel
    
    #Define dashboards and panels
    Dashboard(
        "app",
        "App",
        [
            DashboardPanel("fan", title="CPU fan")
        ],
        is_default=True
    )
    
    Dashboard(
        "system",
        "System",
        [
            DashboardPanel("cpu-load"),
            DashboardPanel("cpu-temp")
        ]
    )
    
    from kervi.sensors.sensor import Sensor
    from kervi.devices.platforms.common.sensors.cpu_use import CPULoadSensorDeviceDriver
    from kervi.devices.platforms.common.sensors.cpu_temp import CPUTempSensorDeviceDriver
    from kervi.devices.sensors.dummy_sensor import DummySensorDeviceDriver
    
    #build in sensor that measures cpu use
    SENSOR_CPU_LOAD = Sensor("CPULoadSensor", "CPU", CPULoadSensorDeviceDriver())
    
    #link to sys area top right
    SENSOR_CPU_LOAD.link_to_dashboard("*", "header_right")
    
    #link to a panel, show value in panel header and chart in panel body
    SENSOR_CPU_LOAD.link_to_dashboard("system", "cpu-load", type="value", link_to_header=True)
    SENSOR_CPU_LOAD.link_to_dashboard("system", "cpu-load", type="chart")

    #build in sensor that measures cpu temperature
    SENSOR_CPU_TEMP = Sensor("CPUTempSensor", "", DummySensorDeviceDriver())
    SENSOR_CPU_TEMP.link_to_dashboard("system", "cpu-temp", type="value", link_to_header=True)
    SENSOR_CPU_TEMP.link_to_dashboard("system", "cpu-temp", type="chart")
    
    from kervi.controllers.controller import Controller, NumberValue
    from kervi.actions import action
    class FanController(Controller):
        def __init__(self):
            Controller.__init__(self, "fan_controller", "Fan")
            self.type = "fan"

            self.temp = self.inputs.add("temp", "Temperature", NumberValue)
            self.temp.min = 0
            self.temp.max = 150

            self.trigger_temp = self.inputs.add("trigger_temp", "Trigger temperature", NumberValue)
            self.trigger_temp.min = 0
            self.trigger_temp.max = 100
            #remember the value when app restarts
            self.trigger_temp.persist_value = True

            self.max_temp = self.inputs.add("max_temp", "Max speed temperature", NumberValue)
            self.max_temp.min = 0
            self.max_temp.max = 100
            #remember the value when app restarts
            self.max_temp.persist_value = True

            #The only output from this controller is the speed of the fan
            self.fan_speed = self.outputs.add("fan_speed", "Fanspeed", NumberValue)

            #private flag that indicate the controller is active and monitors temp and set speed.
            self._active = True

        #action that starts the active monitoring of the temperature input
        @action
        def active(self):
            self._active = True
            self._calc_fan_speed()
        
        #action interrupt call this and the controller stops monitoring the temperature input
        @active.set_interrupt
        def stop(self):
            self._active = False
            self._calc_fan_speed()

        def _calc_fan_speed(self):
            if self._active:
                temp = self.temp.value - self.trigger_temp.value
                if temp <= 0:
                    self.fan_speed.value = 0
                else:
                    max_span = self.max_temp.value - self.trigger_temp.value
                    speed = (temp / max_span) * 100
                    if speed > 100:
                        speed = 100
                    self.fan_speed.value = speed
            else:
                self.fan_speed.value = 0
        
        #called by the framework when a input changes
        def input_changed(self, changed_input):
            self._calc_fan_speed()

    FAN_CONTROLLER = FanController()

    #link the fan controllers temp input to cpu temperature sensor
    FAN_CONTROLLER.temp.link_to(SENSOR_CPU_TEMP)
    
    #link the other fan controller inputs to dashboard
    FAN_CONTROLLER.active.link_to_dashboard("app", "fan", type="button", button_text=None, button_icon="arrow-up", label=None, interrupt_enabled=True)
    
    FAN_CONTROLLER.trigger_temp.link_to_dashboard("app", "fan")
    FAN_CONTROLLER.max_temp.link_to_dashboard("app", "fan")
    FAN_CONTROLLER.fan_speed.link_to_dashboard("app", "fan")

    
    
    #link the fan controller to a DC motor on controlled by a Adafruit motor hat
    #from kervi.devices.motors.adafruit_i2c_motor_hat import AdafruitMotorHAT
    #MOTOR_CONTROLLER = AdafruitMotorHAT()
    #MOTOR_CONTROLLER.dc_motors[2].speed.link_to(FAN_CONTROLLER.fan_speed)

    APP.run()