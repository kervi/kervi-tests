if __name__ == '__main__':
    from kervi.application import Application
    APP = Application()

    #add dashboard and panel
    from kervi.dashboards import Dashboard, DashboardPanel
    DASHBOARD = Dashboard("dahsboard.ctrl", "Controller test", is_default=True)
    DASHBOARD.add_panel(DashboardPanel("textinput", columns=2, rows=4, title="text Width 0"))
    DASHBOARD.add_panel(DashboardPanel("text_inline", columns=3, rows=4, title="text inline"))
    DASHBOARD.add_panel(DashboardPanel("log", columns=3, rows=4, title="Log", user_log=True))

    DASHBOARD = Dashboard("dahsboard.ctrlx", "Controller testx", is_default=True)
    

    #define a light controller
    from kervi.hal import GPIO
    from kervi.controllers.controller import Controller
    from kervi.values import DateTimeValue
    from kervi.messaging import Messaging

    class TestController(Controller):
        def __init__(self):
            Controller.__init__(self, "controller.test", "test")
            self.type = "test"

            #define an input and link it to the dashboard panel
            self.input1 = self.inputs.add("d1", "DateTime 1", DateTimeValue)
            self.input1.link_to_dashboard("dahsboard.ctrl", "textinput")

            self.input2 = self.inputs.add("d2", "DateTime 2", DateTimeValue)
            self.input2.link_to_dashboard("dahsboard.ctrl", "textinput", type="date", input_size=None)

            self.input3 = self.inputs.add("d3", "DateTime 3", DateTimeValue)
            self.input3.link_to_dashboard("dahsboard.ctrl", "textinput", type="time", input_size=75)

        def input_changed(self, changed_input):
            Messaging.send_message("input changed:{0} value:{1}".format(changed_input.value_id, changed_input.value))

    TestController()

    APP.run()