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
    from kervi.controllers.controller import Controller, UIDateTimeControllerInput

    class TestController(Controller):
        def __init__(self):
            Controller.__init__(self, "controller.test", "test")
            self.type = "test"

            #define an input and link it to the dashboard panel
            input1 = UIDateTimeControllerInput("text1", "date input 1", "date", self)
            input1.link_to_dashboard("dahsboard.ctrl", "textinput")

            input2 = UIDateTimeControllerInput("text2", "time input 1", "time", self)
            input2.link_to_dashboard("dahsboard.ctrl", "textinput", input_size=None)

            input3 = UIDateTimeControllerInput("text3", "time input 1", "time", self)
            input3.link_to_dashboard("dahsboard.ctrl", "textinput", input_size=75)

        def input_changed(self, changed_input):
            self.user_log_message("input changed:{0} value:{1}".format(changed_input.input_id, changed_input.value))

    TestController()

    APP.run()