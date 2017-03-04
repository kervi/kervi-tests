if __name__ == '__main__':
    from kervi.bootstrap import Application
    APP = Application()

    #add dashboard and panel
    from kervi.dashboard import Dashboard, DashboardPanel
    DASHBOARD = Dashboard("dahsboard.ctrl", "Controller test", is_default=True)
    DASHBOARD.add_panel(DashboardPanel("switch", columns=2, rows=4, title="Switch Width 0"))
    DASHBOARD.add_panel(DashboardPanel("switch_inline", columns=3, rows=4, title="Switch inline"))
    DASHBOARD.add_panel(DashboardPanel("log", columns=3, rows=4, title="Log", user_log=True))

    DASHBOARD = Dashboard("dahsboard.ctrlx", "Controller testx", is_default=True)
    

    #define a light controller
    from kervi.hal import GPIO
    from kervi.controller import Controller, UISwitchButtonControllerInput, UINumberControllerInput

    class TestController(Controller):
        def __init__(self):
            Controller.__init__(self, "controller.test", "test")
            self.type = "test"

            #define an input and link it to the dashboard panel
            switch_button = UISwitchButtonControllerInput("switchbtn", "Switch", self)
            switch_button.link_to_dashboard("dahsboard.ctrl", "switch")
            
            switch_button1 = UISwitchButtonControllerInput("switchbtn1", "Switch", self)
            switch_button1.link_to_dashboard("dahsboard.ctrl", "switch", label_icon="lightbulb-o")
            
            switch_button2 = UISwitchButtonControllerInput("switchbtn2", "Switch 1", self)
            switch_button2.link_to_dashboard("dahsboard.ctrl", "switch", label_icon="lightbulb-o", label=None)
            
            switch_button2a = UISwitchButtonControllerInput("switchbtn2a", "Switch 1", self)
            switch_button2a.link_to_dashboard("dahsboard.ctrl", "switch", label_icon="lightbulb-o", label="label text")
            
            
            switch_button3 = UISwitchButtonControllerInput("switchbtn3", "Switch", self)
            switch_button3.link_to_dashboard("dahsboard.ctrl", "switch", on_text="1", off_text="0")
            
            switch_button4 = UISwitchButtonControllerInput("switchbtn4", "Switch", self)
            switch_button4.link_to_dashboard("dahsboard.ctrl", "switch", on_text=None, off_text=None, on_icon="toggle-on", off_icon="toggle-off", flat=True)

            #inline

            switch_button5 = UISwitchButtonControllerInput("switchbtn5", "Switch", self)
            switch_button5.link_to_dashboard("dahsboard.ctrl", "switch_inline", inline=True)
            
            switch_button6 = UISwitchButtonControllerInput("switchbtn6", "Switch", self)
            switch_button6.link_to_dashboard("dahsboard.ctrl", "switch_inline", inline=True, label=None, label_icon="lightbulb-o")

            switch_button7 = UISwitchButtonControllerInput("switchbtn7", "Switch", self)
            switch_button7.link_to_dashboard("dahsboard.ctrl", "switch_inline", inline=True, label=None)
            


            # level_input = UINumberControllerInput("lightctrl.level", "Level", self)
            # level_input.min = 0
            # level_input.max = 100
            # level_input.value = 100
            # level_input.link_to_dashboard("system", "light")

            

        def input_changed(self, changed_input):
            self.user_log_message("input changed:{0} value:{1}".format(changed_input.input_id, changed_input.value))

    TestController()

    APP.run()