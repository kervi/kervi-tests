if __name__ == '__main__':
    from kervi.application import Application
    APP = Application()

    #add dashboard and panel
    from kervi.dashboard import Dashboard, DashboardPanel
    DASHBOARD = Dashboard("dashboard", "Dynamic number test", is_default=True)
    DASHBOARD.add_panel(DashboardPanel("number", columns=2, rows=2, title="number Width 0"))
    DASHBOARD.add_panel(DashboardPanel("number_inline", columns=3, rows=3, title="number inline"))
    DASHBOARD.add_panel(DashboardPanel("number_chart", columns=4, rows=3))
    DASHBOARD.add_panel(DashboardPanel("log", columns=3, rows=4, title="Log", user_log=True))


    from kervi.sensor import Sensor
    from kervi_devices.platforms.common.sensors.cpu_use import CPULoadSensorDeviceDriver
    cpu_sensor = Sensor("CPULoadSensor","CPU", CPULoadSensorDeviceDriver())
    cpu_sensor.link_to_dashboard("dashboard", "number_chart", type="chart")
    cpu_sensor.link_to_dashboard("dashboard", "number_chart", link_to_header=True)
    cpu_sensor.link_to_dashboard("*", "header_right")
    


    from kervi.hal import GPIO
    from kervi.controller import Controller
    from kervi.values import DynamicNumber

    class TestController(Controller):
        def __init__(self):
            Controller.__init__(self, "controller.test", "test")
            self.type = "test"

            #define an input and link it to the dashboard panel
            self.test_number = self.inputs.add("test_number", "Number", DynamicNumber)
            
            self.test_number.link_to_dashboard("dashboard", "number", label="xy")
            self.test_number.link_to_dashboard("dashboard", "number", label="#", label_icon="lightbulb-o")


            self.test_number.link_to_dashboard("dashboard", "number_inline", inline=True, label="#", label_icon="lightbulb-o")
            
            
            #self.test_number.link_to_dashboard("dashboard", "number_chart", type="chart")


        def input_changed(self, changed_input):
            self.user_log_message("input changed:{0} value:{1}".format(changed_input.input_id, changed_input.value))

    ctrl = TestController()
    #ctrl.link_to_dashboard("dashboard", "number")

    APP.run()