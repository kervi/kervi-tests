if __name__ == '__main__':
    from kervi.bootstrap import Application
    from kervi import tasks
    APP = Application()

    #add dashboard and panel
    from kervi.dashboard import Dashboard, DashboardPanel
    DASHBOARD = Dashboard("dashboard.ctrl", "Controller Buttons", is_default=True)
    DASHBOARD.add_panel(DashboardPanel("steering", columns=2, rows=2, title="steering"))
    DASHBOARD.add_panel(DashboardPanel("ctrl", columns=3, rows=4, title="Controller"))
    DASHBOARD.add_panel(DashboardPanel("log", columns=3, rows=4, title="Log", user_log=True))

    #define a light controller
    from kervi.hal import GPIO
    from kervi.controller import Controller, UIButtonControllerInput
    from kervi.steering import MotorSteering
    from kervi_devices.motors.dummy_motor_driver import DummyMotorBoard

    MOTOR_BOARD = DummyMotorBoard()
    STEERING = MotorSteering("steering", "motor steering", MOTOR_BOARD.dc_motors[0], MOTOR_BOARD.dc_motors[1])
    STEERING.link_to_dashboard("dashboard.ctrl", "steering")

    class TestController(Controller):
        def __init__(self):
            Controller.__init__(self, "controller.test", "test")
            self.type = "test"

            #define an input and link it to the dashboard panel
            button = UIButtonControllerInput("switchbtn", "Switch", self)
            button.link_to_dashboard("dashboard.ctrl", "ctrl")

        def input_changed(self, changed_input):
            self.user_log_message("input changed:{0} value:{1}".format(changed_input.input_id, changed_input.value))
            tasks.run_task("run", 10, -50,100)

    TestController()

    APP.run()