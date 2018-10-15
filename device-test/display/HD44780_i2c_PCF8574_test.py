if __name__ == '__main__':
    from kervi.application import Application
    APP = Application()

    #add dashboard and panel
    from kervi.dashboards import Dashboard, DashboardPanel
    DASHBOARD = Dashboard("dashboard.ctrl", "Adafruit char lcd test", is_default=True)
    DASHBOARD.add_panel(DashboardPanel("input", columns=2, rows=4, title="input"))
    DASHBOARD.add_panel(DashboardPanel("log", columns=3, rows=4, title="Log", user_log=True))

    #define a light controller
    from kervi.hal import GPIO
    from kervi.controllers import Controller
    from kervi.values import *
    from kervi.devices.displays.HD44780_i2c_PCF8574 import CharLCDDeviceDriver

    class TestController(Controller):
        def __init__(self):
            Controller.__init__(self, "controller.test", "test")
            self.type = "test"

            self.lcd = CharLCDDeviceDriver()
            self.lcd.enable_display(True)
            self.lcd.message("test")
            self.lcd.set_backlight(True)

            self.inputs.add("text", "LCD text", StringValue)
            self.inputs["text"].link_to_dashboard("dashboard.ctrl", "input")

        def input_changed(self, changed_input):
            self.lcd.message(changed_input.value)

        def exit(self):
            self.lcd.message("")
            self.lcd.set_backlight(False)
            self.lcd.enable_display(False)
            
    TestController()

    APP.run()
