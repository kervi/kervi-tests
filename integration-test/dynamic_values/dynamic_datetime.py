if __name__ == '__main__':
    from kervi.application import Application
    APP = Application()

    #add dashboard and panel
    from kervi.dashboards import Dashboard, DashboardPanel
    DASHBOARD = Dashboard("dahsboard.ctrl", "Controller test", is_default=True)
    DASHBOARD.add_panel(DashboardPanel("textinput", title="date time value", width="50%"))
    DASHBOARD.add_panel(DashboardPanel("text_inline", title="inline"))
    DASHBOARD.add_panel(DashboardPanel("log", title="Log", user_log=True))
 

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
            self.input1.persist_value = True
            self.input1.link_to_dashboard("dahsboard.ctrl", "textinput")

            self.input2 = self.inputs.add("d2", "DateTime 2", DateTimeValue)
            self.input2.link_to_dashboard("dahsboard.ctrl", "textinput", type="date", input_size=None)

            self.input3 = self.inputs.add("d3", "DateTime 3", DateTimeValue)
            self.input3.link_to_dashboard("dahsboard.ctrl", "textinput", type="time", input_size=75)

        def input_changed(self, changed_input):
            Messaging.send_message(changed_input.value, source_id=changed_input.component_id, source_name=changed_input.name)
            Messaging.send_message(changed_input.date, source_id=changed_input.component_id, source_name=changed_input.name)
            Messaging.send_message(changed_input.time, source_id=changed_input.component_id, source_name=changed_input.name)

    TestController()

    APP.run()