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
    DASHBOARD = Dashboard("dashboard", "Dynamic number test", is_default=True)
    DASHBOARD.add_panel(DashboardPanel("number", width=33, title="Number"))
    DASHBOARD.add_panel(DashboardPanel("number_inline", title="number inline"))
    DASHBOARD.add_panel(DashboardPanel("number_gauge", width=20))
    
    DASHBOARD.add_panel(DashboardPanel("number_chart"))
    DASHBOARD.add_panel(DashboardPanel("number_chart_x", width=100))
    DASHBOARD.add_panel(DashboardPanel("log", title="Log", user_log=True))


    from kervi.sensors import Sensor
    from kervi.devices.sensors.system import CPULoadSensorDeviceDriver
    cpu_sensor = Sensor("CPULoadSensor","CPU", CPULoadSensorDeviceDriver())
    cpu_sensor.link_to_dashboard("dashboard", "number_chart", type="chart")
    cpu_sensor.link_to_dashboard("dashboard", "number_chart", link_to_header=True)
    cpu_sensor.link_to_dashboard("*", "header_right", show_sparkline=True)
    
    cpu_sensor.link_to_dashboard(
        "dashboard", 
        "number_chart_x", 
        type="chart", 
        chart_grid=False, 
        chart_buttons=False,
        label=False,
        #chart_fill=False,
        chart_point=0
    )
    

    from kervi.devices.sensors.dummy_sensor import DummySensorDeviceDriver, DummyMultiDimSensorDeviceDriver
    BATTERY_SENSOR = Sensor("Battery","Battery", DummySensorDeviceDriver())
    BATTERY_SENSOR.set_ui_parameter("value_icon", [
        {
            "range":[0, 5],
            "icon":"battery-empty"
        },
        {
            "range":[5, 25],
            "icon":"battery-quarter"
        },
        {
            "range":[20, 50],
            "icon":"battery-half"
        },
        {
            "range":[5, 75],
            "icon":"battery-three-quarters"
        },
        {
            "range":[75, 100],
            "icon":"battery-full"
        }
    ])
    BATTERY_SENSOR.link_to_dashboard("dashboard", "number_gauge", link_to_header=True, display_unit=False, show_sparkline=False, show_value=False)

    
    TEST_SENSOR = Sensor(
        "chart_test",
        "Chart test", 
        DummySensorDeviceDriver(min=-100), 
        polling_interval=10
    )
    TEST_SENSOR.link_to_dashboard(
        "dashboard", 
        type="chart", 
        #chart_grid=False, 
        chart_buttons=False,
        label=False,
        #chart_fill=False,
        chart_point=3
    )

    from kervi.hal import GPIO
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
            
            self.test_number.link_to_dashboard("dashboard", "number", label="xy")
            self.test_number.link_to_dashboard("dashboard", "number", label="#", label_icon="lightbulb-o")


            self.test_number.link_to_dashboard("dashboard", "number_inline", inline=True, label="#", label_icon="lightbulb-o")
            
            self.test_number.link_to_dashboard("dashboard", "number_gauge", type="radial_gauge")
            self.test_number.add_error_range((0, 10), "l error message", channels=["user_log", "email"])
            self.test_number.add_warning_range((10, 20), "l warning message")
            self.test_number.add_warning_range((80, 90), "h warning message")
            self.test_number.add_normal_range((20, 80), "normal")
            self.test_number.add_error_range((90, 100), "h error message", channels=["user_log", "email"])

            
            #self.test_number.link_to_dashboard("dashboard", "number_chart", type="chart")


        def input_changed(self, changed_input):
            Messaging.send_message("input changed:{0} value:{1}".format(changed_input.value_id, changed_input.value))

    ctrl = TestController()
    #ctrl.link_to_dashboard("dashboard", "number")

    APP.run()