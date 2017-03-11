if __name__ == '__main__':
    from kervi.bootstrap import Application
    APP = Application()

    #add dashboard and panel
    from kervi.dashboard import Dashboard, DashboardPanel
    DASHBOARD = Dashboard("dashboard.ctrl", "PCF8591 test", is_default=True)
    DASHBOARD.add_panel(DashboardPanel("input", columns=2, rows=4, title="input"))
    DASHBOARD.add_panel(DashboardPanel("log", columns=3, rows=4, title="Log", user_log=True))

    #define a light controller
    from kervi.hal import GPIO
    from kervi.controller import Controller, UINumberControllerInput, AnalogGPIOControllerInput
    from kervi_devices.gpio import PCF8591

    class TestController(Controller):
        def __init__(self):
            Controller.__init__(self, "controller.test", "test")
            self.type = "test"

            self.gpio = PCF8591.PCF8591Driver()
            self.AIN0 = AnalogGPIOControllerInput("ain0", "AIN0", self, PCF8591.AIN0, gpio_device=self.gpio)
            self.AIN0.link_to_dashboard("dashboard.ctrl", "input", input_size=25)

        def input_changed(self, changed_input):
            self.user_log_message("input changed:{0} value:{1}".format(changed_input.input_id, changed_input.value))

    APP.run()