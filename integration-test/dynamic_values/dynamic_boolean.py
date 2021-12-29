if __name__ == '__main__':
    from kervi.application import Application
    APP = Application({
        "network":{
            "ip": "127.0.0.1",
            "ipc_root_address": "127.0.0.1",
            "ws_port": 9000,
        }        
    })

    #add dashboard and panel
    from kervi.dashboards import Dashboard, DashboardPanel
    DASHBOARD = Dashboard("dashboard", "Dynamic boolean test", is_default=True)
    DASHBOARD.add_panel(DashboardPanel("boolean", title="Boolean"))
    DASHBOARD.add_panel(DashboardPanel("boolean_inline", title="boolean inline"))
    DASHBOARD.add_panel(DashboardPanel("log", title="Log", user_log=True))

    from kervi.hal import GPIO
    from kervi.controllers import Controller
    from kervi.values import BooleanValue
    from kervi.messaging import Messaging

    class TestController(Controller):
        def __init__(self):
            Controller.__init__(self, "controller.test", "test")
            self.type = "test"

            #define an input and link it to the dashboard panel
            self.inputs.add("boolean", "Boolean", BooleanValue)
            self.inputs["boolean"].link_to_dashboard("dashboard", "boolean")
            self.inputs["boolean"].link_to_dashboard("dashboard", "boolean", label="1", label_icon="bulb", on_text="active", off_text="inactive")
            self.inputs["boolean"].link_to_dashboard(
                "dashboard",
                "boolean",
                label="2",
                on_icon="left",
                on_text=None,
                off_icon="right",
                off_text=None
                
            )

            self.inputs["boolean"].link_to_dashboard(
                "dashboard",
                "boolean",
                label="3",
                on_icon="left",
                on_text="Activex",
                off_icon="right",
                off_text="Passivex"
                
            )


            self.inputs["boolean"].link_to_dashboard(
                "dashboard",
                "boolean",
                label="4",
                type="button",
                button_text=None,
                on_icon="left",
                off_icon="right",
                on_text="ON",
                off_text="OFF"
            )

            self.inputs["boolean"].link_to_dashboard(
                "dashboard",
                "boolean",
                label="5",
                type="button"
            )

            self.inputs["boolean"].link_to_dashboard(
                "dashboard",
                "boolean",
                label="6",
                button_icon="plus",
                button_text="Button text",
                type="button"
            )

            self.inputs["boolean"].link_to_dashboard(
                "dashboard",
                "boolean",
                label="7",
                button_icon="left",
                button_text="Button text",
                type="button"
            )

            self.inputs["boolean"].link_to_dashboard(
                "dashboard",
                "boolean",
                label="8",
                type="button",
                button_text=None,
                on_icon="left",
                off_icon="right",
                on_text=None,
                off_text=None
            )

            self.inputs["boolean"].link_to_dashboard(
                "dashboard",
                "boolean_inline",
                label="1 inline",
                on_icon="left",
                on_text=None,
                off_icon="right",
                off_text=None,
                inline=True
                
            )

            self.inputs["boolean"].link_to_dashboard(
                "dashboard",
                "boolean_inline",
                label="2 inline btn",
                type="button",
                inline=True
            )

            self.inputs["boolean"].link_to_dashboard(
                "dashboard",
                "boolean_inline",
                label="3 inline btn",
                type="button",
                button_icon="left",
                button_text=None,
                inline=True
            )

        def input_changed(self, changed_input):
            Messaging.send_message("input changed:{0} value:{1}".format(changed_input.value_id, changed_input.value))

    TestController()

    APP.run()