
if __name__ == '__main__':
    from kervi.application import Application
    APP = Application({
        "application": {
            "id":"app_5",
            "name":"Kervi io app 5",
            "appKey":"1234",
        },
        "discovery":{
            "enabled": False
        },
        "log":{
            "file":"kervi-module.log"
        },
        "network":{
            "ip": "127.0.0.1",
            "ip_module_port": 1100,
            "ipc_root_port": 1200,
            "ipc_root_address": "127.0.0.1",
            "ws_port": "9001"
        },
        "plugins":{
            "kervi.plugin.routing.kervi_io":{
                "enabled": True,
                "api_user": "86a2a8aa634d42a09b90e2eb6390cbf6",
                "api_password": "5f0b164f424040658264af22c0d8f14a",
                "api_channel": "20bddf88a4434e99ba0e014de2b875c7"
            }
        }
    })

    
    from kervi.sensors import Sensor
    from kervi.devices.sensors.system import CPULoadSensorDeviceDriver

    SENSOR_1 = Sensor("module_CPULoadSensor", "CPU 2", CPULoadSensorDeviceDriver())
    SENSOR_1.link_to_dashboard(type="value", link_to_header=True)
    SENSOR_1.link_to_dashboard(type="chart")

    from kervi.controllers import Controller
    from kervi.values import NumberValue
    from kervi.messaging import Messaging

    class TestController(Controller):
        def __init__(self):
            Controller.__init__(self, "controller.test", "test")
            self.type = "test"

            #define an input and link it to the dashboard panel
            self.test_number = self.inputs.add("test_number", "Number", NumberValue)
            self.test_number.unit = "%"
            
            self.test_number.link_to_dashboard( label="xy")
            self.test_number.link_to_dashboard( label="#", label_icon="lightbulb-o")


            self.test_number.link_to_dashboard( inline=True, label="#", label_icon="lightbulb-o")
            
            self.test_number.link_to_dashboard( type="radial_gauge")
            self.test_number.add_error_range((0, 10), "l error message", channels=["user_log", "email"])
            self.test_number.add_warning_range((10, 20), "l warning message")
            self.test_number.add_warning_range((80, 90), "h warning message")
            self.test_number.add_normal_range((20, 80), "normal")
            self.test_number.add_error_range((90, 100), "h error message", channels=["user_log", "email"])

            
            #self.test_number.link_to_dashboard("dashboard", "number_chart", type="chart")


        def input_changed(self, changed_input):
            Messaging.send_message("input changed:{0} value:{1}".format(changed_input.value_id, changed_input.value))

    ctrl = TestController()

    APP.actions.shutdown.link_to_dashboard("*", "header_right", inline=True, label=None, button_text="App shutdown")

    APP.run()