if __name__ == '__main__':
    from kervi.bootstrap import Application
    APP = Application()

    #add dashboard and panel
    from kervi.dashboard import Dashboard, DashboardPanel
    DASHBOARD = Dashboard("dahsboard.ctrl", "Controller test", is_default=True)
    DASHBOARD.add_panel(DashboardPanel("numberinput", columns=2, rows=4, title="number Width 0"))
    DASHBOARD.add_panel(DashboardPanel("number_inline", columns=3, rows=4, title="number inline"))
    DASHBOARD.add_panel(DashboardPanel("log", columns=3, rows=4, title="Log", user_log=True))

    DASHBOARD = Dashboard("dahsboard.ctrlx", "Controller testx", is_default=True)
    

    #define a light controller
    from kervi.hal import GPIO
    from kervi.controller import Controller, UINumberControllerInput

    class TestController(Controller):
        def __init__(self):
            Controller.__init__(self, "controller.test", "test")
            self.type = "test"

            #define an input and link it to the dashboard panel
            input1 = UINumberControllerInput("input1", "num input 1", self)
            input1.link_to_dashboard("dahsboard.ctrl", "numberinput")

            input2 = UINumberControllerInput("input2", "num input 1", self)
            input2.link_to_dashboard("dahsboard.ctrl", "numberinput", input_size=25 )
            
            input2.link_to_dashboard("dahsboard.ctrl", "number_inline", input_size=25, inline=True )


        def input_changed(self, changed_input):
            self.user_log_message("input changed:{0} value:{1}".format(changed_input.input_id, changed_input.value))

    TestController()

    APP.run()