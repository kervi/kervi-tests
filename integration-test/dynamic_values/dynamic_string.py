if __name__ == '__main__':
    from kervi.application import Application
    APP = Application()

    #add dashboard and panel
    from kervi.dashboards import Dashboard, DashboardPanel
    DASHBOARD = Dashboard(
        "dashboard",
        "Controller test",
        [
        #     DashboardPanel("text", title="text Width 0"),
        #     DashboardPanel("text_inline",  title="text inline"),
        #     DashboardPanel("log", title="Log", user_log=True)
        ],
        is_default=True
    )

    from kervi.controllers.controller import Controller
    from kervi.values import StringValue
    from kervi.messaging import Messaging

    class TestController(Controller):
        def __init__(self):
            Controller.__init__(self, "controller.test", "test")
            self.type = "test"

            self.test_string = self.inputs.add("test_string", "String", StringValue)
            self.test_string.persist_value = True
            self.test_string.link_to_dashboard()
            self.test_string.link_to_dashboard(label="#", label_icon="lightbulb-o")
            self.test_string.link_to_dashboard(label="#", label_icon="lightbulb-o", inline=True)
            self.test_string.link_to_dashboard(label=None, input_size="30px")
            self.test_string.link_to_dashboard(label="30px", input_size="30px")
            self.test_string.link_to_dashboard(label="30%", input_size="30%")
            self.test_string.link_to_dashboard(label="5rem", input_size="5rem")
            self.test_string.link_to_dashboard(label="5rem", input_size="5rem", inline=True)
            self.test_string.link_to_dashboard(label=None, inline=True)

            self.test_string_out = self.outputs.add("test_string_out", "String out", StringValue)
            self.test_string_out.link_to_dashboard()
            self.test_string_out.link_to_dashboard(inline=True)
            self.test_string_out.value = "a test"

        def input_changed(self, changed_input):
            Messaging.send_message("input changed:{0} value:{1}".format(changed_input.component_id, changed_input.value))

    TestController()

    APP.run()