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
    from kervi.controller import Controller
    from kervi.steering import MotorSteering
    from kervi_devices.motors.dummy_motor_driver import DummyMotorBoard

    MOTOR_BOARD = DummyMotorBoard()
    STEERING = MotorSteering("steering", "motor steering")
    STEERING.link_to_dashboard("dashboard.ctrl", "steering")

    STEERING.outputs["left_speed"].link_to(MOTOR_BOARD.dc_motors[0].speed)
    STEERING.outputs["right_speed"].link_to(MOTOR_BOARD.dc_motors[1].speed)

    APP.run()