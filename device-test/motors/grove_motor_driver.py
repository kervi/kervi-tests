if __name__ == '__main__':
    from kervi.application import Application
    APP = Application()

    #add dashboard and panel
    from kervi.dashboard import Dashboard, DashboardPanel
    DASHBOARD = Dashboard("dashboard", "Grove motor driver dc test", is_default=True)
    DASHBOARD.add_panel(DashboardPanel("input", columns=2, rows=4, title="input"))
    
    #define a light controller
    #from kervi.hal import GPIO
    from kervi.controller import Controller
    from kervi_devices.motors.grove_i2c_motor_driver import GroveMotorController

    motor_controller = GroveMotorController(0x0f, 1)
    motor_controller.dc_motors[0].speed.link_to_dashboard("dashboard", "input")
    motor_controller.dc_motors[1].speed.link_to_dashboard("dashboard", "input")
    

    

    APP.run()