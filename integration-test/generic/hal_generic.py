if __name__ == '__main__':
    from kervi.bootstrap import Application
    APP = Application()

    #add dashboard and panel
    from kervi.dashboard import Dashboard, DashboardPanel
    DASHBOARD = Dashboard("dahsboard.ctrl", "Controller Buttons", is_default=True)
    DASHBOARD.add_panel(DashboardPanel("button", columns=2, rows=4, title="button Width 0"))
    DASHBOARD.add_panel(DashboardPanel("button_inline", columns=3, rows=4, title="button inline"))
    DASHBOARD.add_panel(DashboardPanel("log", columns=3, rows=4, title="Log", user_log=True))
    
    #define a light controller
    from kervi.hal import GPIO
    from kervi.controller import Controller, UIButtonControllerInput

    class TestController(Controller):
        def __init__(self):
            Controller.__init__(self, "controller.test", "test")
            self.type = "test"

            #define an input and link it to the dashboard panel
            button = UIButtonControllerInput("switchbtn", "Switch", self)
            button.link_to_dashboard("dahsboard.ctrl", "button")
            
            GPIO[1].set(True)

            # level_input = UINumberControllerInput("lightctrl.level", "Level", self)
            # level_input.min = 0
            # level_input.max = 100
            # level_input.value = 100
            # level_input.link_to_dashboard("system", "light")

            

        def input_changed(self, changed_input):
            self.user_log_message("input changed:{0} value:{1}".format(changed_input.input_id, changed_input.value))

    TestController()

    APP.run()