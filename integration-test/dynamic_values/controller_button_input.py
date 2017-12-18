if __name__ == '__main__':
    from kervi.application import Application
    APP = Application()

    #add dashboard and panel
    from kervi.dashboards.dashboard import Dashboard, DashboardPanel
    DASHBOARD = Dashboard("dahsboard.ctrl", "Controller Buttons", is_default=True)
    DASHBOARD.add_panel(DashboardPanel("button", columns=2, rows=4, title="button Width 0"))
    DASHBOARD.add_panel(DashboardPanel("button_inline", columns=3, rows=4, title="button inline"))
    DASHBOARD.add_panel(DashboardPanel("log", columns=3, rows=4, title="Log", user_log=True))

    DASHBOARD = Dashboard("dahsboard.ctrlx", "Controller testx", is_default=True)
    

    #define a light controller
    from kervi.hal import GPIO
    from kervi.controllers.controller import Controller, UIButtonControllerInput

    class TestController(Controller):
        def __init__(self):
            Controller.__init__(self, "controller.test", "test")
            self.type = "test"

            #define an input and link it to the dashboard panel
            button = UIButtonControllerInput("switchbtn", "Switch", self)
            button.link_to_dashboard("dahsboard.ctrl", "button")
            
            button1 = UIButtonControllerInput("switchbtn1", "Switch 1", self)
            button1.link_to_dashboard("dahsboard.ctrl", "button", button_icon="lightbulb-o", button_text="btn text")
            
            button2 = UIButtonControllerInput("switchbtn2", "button 1", self)
            button2.link_to_dashboard("dahsboard.ctrl", "button", button_icon="lightbulb-o", label="label", label_icon="lightbulb-o")
            button2.link_to_dashboard("dahsboard.ctrl", "button_inline", button_icon="lightbulb-o", label="label", label_icon="lightbulb-o")
            
            
            #inline

            button5 = UIButtonControllerInput("switchbtn5", "Switch", self)
            button5.link_to_dashboard("dahsboard.ctrl", "button_inline", inline=True, button_icon="lightbulb-o")
            
            button6 = UIButtonControllerInput("switchbtn6", "Switch", self)
            button6.link_to_dashboard("dahsboard.ctrl", "button_inline", inline=True, label=False, label_icon="lightbulb-o")

            button7 = UIButtonControllerInput("switchbtn7", "Switch", self)
            button7.link_to_dashboard("dahsboard.ctrl", "button_inline", inline=True, label=False)
            


            # level_input = UINumberControllerInput("lightctrl.level", "Level", self)
            # level_input.min = 0
            # level_input.max = 100
            # level_input.value = 100
            # level_input.link_to_dashboard("system", "light")

            

        def input_changed(self, changed_input):
            self.user_log_message("input changed:{0} value:{1}".format(changed_input.input_id, changed_input.value))

    TestController()

    APP.run()