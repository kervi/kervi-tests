if __name__ == '__main__':
    from kervi.bootstrap import Application
    APP = Application()

    #add dashboard and panel
    from kervi.dashboard import Dashboard, DashboardPanel
    DASHBOARD = Dashboard("dashboard", "Controller test", is_default=True)
    DASHBOARD.add_panel(DashboardPanel("text", columns=2, rows=4, title="text Width 0"))
    DASHBOARD.add_panel(DashboardPanel("text_inline", columns=3, rows=4, title="text inline"))
    DASHBOARD.add_panel(DashboardPanel("log", columns=3, rows=4, title="Log", user_log=True))


    #define a light controller
    from kervi.hal import GPIO
    from kervi.controller import Controller
    from kervi.values import DynamicString


    class TestController(Controller):
        def __init__(self):
            Controller.__init__(self, "controller.test", "test")
            self.type = "test"

            self.test_string = self.inputs.add("test_string", "String", DynamicString)
            self.test_string.link_to_dashboard("dashboard", "text")
            self.test_string.link_to_dashboard("dashboard", "text", label="#", label_icon="lightbulb-o")
            self.test_string.link_to_dashboard("dashboard", "text", label="#", label_icon="lightbulb-o", inline=True)

        def input_changed(self, changed_input):
            self.user_log_message("input changed:{0} value:{1}".format(changed_input.input_id, changed_input.value))

    TestController()

    APP.run()