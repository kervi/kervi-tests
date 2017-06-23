if __name__ == '__main__':
    from kervi.bootstrap import Application
    APP = Application()

    #add dashboard and panel
    from kervi.dashboard import Dashboard, DashboardPanel
    DASHBOARD = Dashboard("dashboard", "Dynamic number test", is_default=True)
    DASHBOARD.add_panel(DashboardPanel("number", columns=2, rows=4, title="number Width 0"))
    DASHBOARD.add_panel(DashboardPanel("number_inline", columns=3, rows=4, title="number inline"))
    DASHBOARD.add_panel(DashboardPanel("log", columns=3, rows=4, title="Log", user_log=True))

    from kervi.hal import GPIO
    from kervi.controller import Controller
    from kervi.values import DynamicNumber

    class TestController(Controller):
        def __init__(self):
            Controller.__init__(self, "controller.test", "test")
            self.type = "test"

            #define an input and link it to the dashboard panel
            self.test_number = self.inputs.add("test_number", "Number", DynamicNumber)
            self.test_number.link_to_dashboard("dashboard", "number")
            self.test_number.link_to_dashboard("dashboard", "number", label="#", label_icon="lightbulb-o")


        def input_changed(self, changed_input):
            self.user_log_message("input changed:{0} value:{1}".format(changed_input.input_id, changed_input.value))

    ctrl = TestController()
    ctrl.link_to_dashboard("dashboard", "number")

    APP.run()