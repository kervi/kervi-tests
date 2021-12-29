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
    DASHBOARD = Dashboard("dashboard", "colortest", is_default=True)
    DASHBOARD.add_panel(DashboardPanel("color", width=25, title="Color"))
    DASHBOARD.add_panel(DashboardPanel("color_inline", title="Color inline"))
    DASHBOARD.add_panel(DashboardPanel("log", title="Log", user_log=True))

    from kervi.controllers import Controller
    from kervi.values import ColorValue
    from kervi.messaging import Messaging

    class TestController(Controller):
        def __init__(self):
            Controller.__init__(self, "controller.test", "test")
            self.type = "test"

            #define an input and link it to the dashboard panel
            self.color = self.inputs.add("color", "Boolean", ColorValue)
            self.color.value = "#000f00"
            self.color.persist_value = True
            self.color.link_to_dashboard("dashboard", "boolean")
            self.color.link_to_dashboard("dashboard", "boolean", label="#", label_icon="lightbulb-o")
            self.color.link_to_dashboard(
                "dashboard",
                "boolean",
                label="#",
            )

            self.inputs["color"].link_to_dashboard(
                "dashboard",
                "color",
                label="#",
                
                
            )


            

            self.inputs["color"].link_to_dashboard(
                "color",
                "color_inline",
                label="#inline",
                inline=True
                
            )

            self.color_out = self.outputs.add("color_out", "Color out", ColorValue)   
            self.color_out.link_to_dashboard()

        def input_changed(self, changed_input):
            Messaging.send_message("input changed:{0} value:{1}".format(changed_input.value_id, changed_input.value))
            self.color_out.value = changed_input.value

    TestController()

    from kervi.sensors import Sensor
    from kervi.devices.sensors.dummy_sensor import DummyColorSensorDeviceDriver
    #from kervi.devices.sensors.TCS34725 import TCS34725DeviceDriver
    sensor = Sensor("color_sensor", "Color sensor", DummyColorSensorDeviceDriver())
    sensor.link_to_dashboard()

    APP.run()