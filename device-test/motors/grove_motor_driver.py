if __name__ == '__main__':
    from kervi.bootstrap import Application
    APP = Application()

    #add dashboard and panel
    from kervi.dashboard import Dashboard, DashboardPanel
    DASHBOARD = Dashboard("dashboard.ctrl", "Grove motor driver dc test", is_default=True)
    DASHBOARD.add_panel(DashboardPanel("input", columns=2, rows=4, title="input"))
    DASHBOARD.add_panel(DashboardPanel("log", columns=3, rows=4, title="Log", user_log=True))

    #define a light controller
    #from kervi.hal import GPIO
    from kervi.controller import Controller, UINumberControllerInput
    from kervi_devices.motors.grove_i2c_motor_driver import GroveMotorController

    class TestController(Controller):
        def __init__(self):
            Controller.__init__(self, "controller.test", "test")
            self.type = "test"

            self.motor_controller = GroveMotorController(0x0f, 1)
            self.motor1 = self.motor_controller.dc_motors[1]
            self.motor2 = self.motor_controller.dc_motors[2]

            self.speed1 = UINumberControllerInput("speed1", "speed 1", self)
            self.speed1.link_to_dashboard("dashboard.ctrl", "input")

            self.speed2 = UINumberControllerInput("speed2", "speed 2", self)
            self.speed2.link_to_dashboard("dashboard.ctrl", "input")

        def input_changed(self, changed_input):
            self.user_log_message("input changed:{0} value:{1}".format(changed_input.input_id, changed_input.value))
            if changed_input == self.speed1:
                self.motor1.set_speed(changed_input.value)
            if changed_input == self.speed2:
                self.motor2.set_speed(changed_input.value)
    TestController()

    APP.run()