if __name__ == '__main__':
    from kervi.bootstrap import Application
    APP = Application()

    #add dashboard and panel
    from kervi.dashboard import Dashboard, DashboardPanel
    DASHBOARD = Dashboard("dashboard", "Dynamic boolean test", is_default=True)
    DASHBOARD.add_panel(DashboardPanel("boolean", columns=2, rows=4, title="Boolean width=0"))
    DASHBOARD.add_panel(DashboardPanel("boolean_inline", columns=3, rows=4, title="boolean inline"))
    DASHBOARD.add_panel(DashboardPanel("log", columns=3, rows=4, title="Log", user_log=True))

    from kervi.hal import GPIO
    from kervi.controller import Controller
    from kervi.values import DynamicBoolean

    class TestController(Controller):
        def __init__(self):
            Controller.__init__(self, "controller.test", "test")
            self.type = "test"

            #define an input and link it to the dashboard panel
            self.inputs.add("boolean", "Boolean", DynamicBoolean)
            self.inputs["boolean"].link_to_dashboard("dashboard", "boolean")
            self.inputs["boolean"].link_to_dashboard("dashboard", "boolean", label="#", label_icon="lightbulb-o")
            self.inputs["boolean"].link_to_dashboard(
                "dashboard",
                "boolean",
                label="#",
                on_icon="chevron-left",
                on_text=None,
                off_icon="chevron-right",
                off_text=None
                
            )
            self.inputs["boolean"].link_to_dashboard(
                "dashboard",
                "boolean",
                label="#",
                type="button"
            )

        def input_changed(self, changed_input):
            self.user_log_message("input changed:{0} value:{1}".format(changed_input.input_id, changed_input.value))

    TestController()

    APP.run()