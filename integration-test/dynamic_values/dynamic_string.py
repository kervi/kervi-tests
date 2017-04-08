if __name__ == '__main__':
    from kervi.bootstrap import Application
    APP = Application()

    #add dashboard and panel
    from kervi.dashboard import Dashboard, DashboardPanel
    DASHBOARD = Dashboard("dahsboard.ctrl", "Controller test", is_default=True)
    DASHBOARD.add_panel(DashboardPanel("textinput", columns=2, rows=4, title="text Width 0"))
    DASHBOARD.add_panel(DashboardPanel("text_inline", columns=3, rows=4, title="text inline"))
    DASHBOARD.add_panel(DashboardPanel("log", columns=3, rows=4, title="Log", user_log=True))

    DASHBOARD = Dashboard("dahsboard.ctrlx", "Controller testx", is_default=True)
    

    #define a light controller
    from kervi.hal import GPIO
    from kervi.controller import Controller, UITextControllerInput

    class TestController(Controller):
        def __init__(self):
            Controller.__init__(self, "controller.test", "test")
            self.type = "test"

            #define an input and link it to the dashboard panel
            input1 = UITextControllerInput("text1", "num input 1", self)
            input1.link_to_dashboard("dahsboard.ctrl", "textinput")

            input2 = UITextControllerInput("text2", "num input 1", self)
            input2.link_to_dashboard("dahsboard.ctrl", "textinput", input_size=None)

            input2 = UITextControllerInput("text2", "num input 1", self)
            input2.link_to_dashboard("dahsboard.ctrl", "textinput", input_size=None)

        def input_changed(self, changed_input):
            self.user_log_message("input changed:{0} value:{1}".format(changed_input.input_id, changed_input.value))

    TestController()

    APP.run()