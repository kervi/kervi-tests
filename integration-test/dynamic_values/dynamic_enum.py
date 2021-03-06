if __name__ == '__main__':
    from kervi.application import Application
    APP = Application()

    #add dashboard and panel
    from kervi.dashboards import Dashboard, DashboardPanel
    #DASHBOARD = Dashboard("dahsboard.ctrl", "Controller test", is_default=True)
    #DASHBOARD.add_panel(DashboardPanel("select", columns=2, rows=4, title="select Width 0"))
    #DASHBOARD.add_panel(DashboardPanel("select_inline", columns=3, rows=4, title="Select inline"))
    #DASHBOARD.add_panel(DashboardPanel("log", columns=3, rows=4, title="Log", user_log=True))

    #DASHBOARD = Dashboard("dahsboard.ctrlx", "Controller testx", is_default=True)
    

    #define a light controller
    from kervi.controllers import Controller
    from kervi.values import EnumValue
    from kervi.messaging import Messaging

    class TestController(Controller):
        def __init__(self):
            Controller.__init__(self, "controller.test", "test")
            self.type = "test"

            #define an input and link it to the dashboard panel
            select = self.inputs.add("select1", "enum ", EnumValue)
            select.add_option("1","option 1", selected=True)
            select.add_option("2","option 2")
            select.add_option("3","option 3")
            select.persist_value = True
            select.link_to_dashboard()
            select.link_to_dashboard(type="buttons")

            #select1 = UISelectControllerInput("select2", "Switch1", self)
            #select1.add_option("1","option 1")
            #select1.add_option("2","option 2", True)
            #select1.add_option("3","option 3")
            #select1.link_to_dashboard("dahsboard.ctrl", "select", label_icon="lightbulb-o")

            #select2 = UISelectControllerInput("select3", "Switch1", self)
            #select2.add_option("1","option 1")
            #select2.add_option("2","option 2", True)
            #select2.add_option("3","option 3")
            #select2.link_to_dashboard("dahsboard.ctrl", "select", inline=True)

        def input_changed(self, changed_input):
            Messaging.send_message("input changed:{0} value:{1}".format(changed_input.value_id, changed_input.value))

    TestController()

    APP.run()