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
    from kervi_devices.motors.PCA9685_i2c_servo import PCA9685ServoBoard

    class TestController(Controller):
        def __init__(self):
            Controller.__init__(self, "controller.test", "test")
            self.type = "test"

            self.motor_controller = PCA9685ServoBoard()
            self.motor1 = self.motor_controller.servo_motors[0]

            self.position = UINumberControllerInput("position", "position", self)
            self.position.link_to_dashboard("dashboard.ctrl", "input")

        def input_changed(self, changed_input):
            self.user_log_message("input changed:{0} value:{1}".format(changed_input.input_id, changed_input.value))
            if changed_input == self.position:
                self.motor1.set_position(changed_input.value)

    TestController()

    APP.run()