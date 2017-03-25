if __name__ == '__main__':
    from kervi.bootstrap import Application
    APP = Application()

    #add dashboard and panel
    from kervi.dashboard import Dashboard, DashboardPanel
    DASHBOARD = Dashboard("dashboard.ctrl", "adafruit motor driver dc test", is_default=True)
    DASHBOARD.add_panel(DashboardPanel("input", columns=2, rows=4, title="input"))
    DASHBOARD.add_panel(DashboardPanel("log", columns=3, rows=4, title="Log", user_log=True))

    #define a light controller
    #from kervi.hal import GPIO
    from kervi.controller import Controller, UINumberControllerInput, UIButtonControllerInput, UISwitchButtonControllerInput
    from kervi_devices.motors.adafruit_i2c_motor_hat import AdafruitMotorHAT

    class TestController(Controller):
        def __init__(self):
            Controller.__init__(self, "controller.test", "test")
            self.type = "test"

            self.motor_controller = AdafruitMotorHAT()
            self.dc_motor = self.motor_controller.dc_motors[0]
            self.stepper_motor = self.motor_controller.stepper_motors[1]

            #print("motor driver:", self.motor_controller.device_name)

            self.speed = UINumberControllerInput("speed", "dc speed", self)
            self.speed.link_to_dashboard("dashboard.ctrl", "input")

            self.step_interval = UINumberControllerInput("step_interval", "step_interval", self)
            self.step_interval.link_to_dashboard("dashboard.ctrl", "input")

            self._step = UIButtonControllerInput("step", "Step", self)
            self._step.link_to_dashboard("dashboard.ctrl", "input")

            self._start_stepper = UISwitchButtonControllerInput("start_stepper", "Start step", self)
            self._start_stepper.link_to_dashboard("dashboard.ctrl", "input")

        def input_changed(self, changed_input):
            self.user_log_message("input changed:{0} value:{1}".format(changed_input.input_id, changed_input.value))
            if changed_input == self.speed:
                self.dc_motor.run(changed_input.value)
            if changed_input == self.step_interval:
                self.stepper_motor.step_interval = changed_input.value
            if changed_input == self._step:
                self.stepper_motor.step(10)
                self.stepper_motor.step(-10)
    TestController()

    APP.run()