# Copyright (c) 2016, Tim Wentzlau
# Licensed under MIT

if __name__ == '__main__':
    from kervi.application import Application
    APP = Application({
        "network":{
            "ip": "127.0.0.1",
            "ipc_root_address": "127.0.0.1",
            "ws_port": 9000,
        },
        "location": {
            # greenwich
            "longitude": 61.563300, 
            "latitude": -6.838634,
            "time_zone": 0
        },
    })

    #add dashboard and panel
    from kervi.dashboards import Dashboard, DashboardPanel
    DASHBOARD = Dashboard("system", "Sensor test", is_default=True)
    DASHBOARD.add_panel(DashboardPanel("multi_sensor", title="Multi sensor"))
    DASHBOARD.add_panel(DashboardPanel("multi_sensor_single", title="Multi sensor single"))
    DASHBOARD.add_panel(DashboardPanel("color_sensor", title="Color sensor single ----xxx---"))
    DASHBOARD.add_panel(DashboardPanel("sun_sensor", title="Sun sensor"))
    DASHBOARD.add_panel(DashboardPanel("gauge", title="Gauge"))
    DASHBOARD.add_panel(DashboardPanel("log", title="Log", user_log=True))

    from kervi.sensors import Sensor
    from kervi.devices.sensors.system import CPULoadSensorDeviceDriver
    from kervi.devices.sensors.dummy_sensor import DummyMultiDimSensorDeviceDriver
    

    cpu_sensor = Sensor("CPULoadSensor","CPU", CPULoadSensorDeviceDriver())
    cpu_sensor.store_to_db = False
    cpu_sensor.link_to_dashboard("*", "header_right", show_sparkline=True)
    cpu_sensor.link_to_dashboard("system", "cpu", type="value", link_to_header=True)
    cpu_sensor.link_to_dashboard("system", "cpu", type="chart")


    multi_sensor = Sensor("MultiSensor", "multi sensor", DummyMultiDimSensorDeviceDriver())
    multi_sensor.store_to_db = False
    multi_sensor.link_to_dashboard("system", "multi_sensor", type="value")

    multi_sensor[0].link_to_dashboard("system", "multi_sensor_single", type="value")
    multi_sensor[1].link_to_dashboard("system", "multi_sensor_single", type="value")
    multi_sensor[2].link_to_dashboard("system", "multi_sensor_single", type="value")

    multi_sensor[0].link_to_dashboard("system", "gauge", type="horizontal_linear_gauge")
    multi_sensor[1].link_to_dashboard("system", "gauge", type="vertical_linear_gauge")

    multi_sensor[2].add_error_range((0, 10), "l error message")
    multi_sensor[2].add_warning_range((10, 20), "l warning message")
    multi_sensor[2].add_warning_range((80, 90), "h warning message")
    multi_sensor[2].add_error_range((90, 100), "h error message", channels=["user_log", "email"])
    #multi_sensor[2].add_normal_range((20, 80), "normal message")
    multi_sensor[2].link_to_dashboard("system", "gauge", type="radial_gauge")

    #multi_sensor.enable.link_to_dashboard()

    from kervi.devices.sensors.dummy_sensor import DummyColorSensorDeviceDriver
    color_sensor = Sensor("color_sensor", "Color", DummyColorSensorDeviceDriver())
    color_sensor.link_to_dashboard("system", "color_sensor")
    color_sensor.link_to_dashboard("system", "color_sensor")
    
    from kervi.devices.sensors.sun import SunSensorDeviceDriver
    sun_sensor = Sensor("sun_sensor", "Sun", SunSensorDeviceDriver())
    #sun_sensor.link_to_dashboard("system", "sun_sensor")
    sun_sensor[0].link_to_dashboard("system", "sun_sensor")
    sun_sensor[1].link_to_dashboard("system", "sun_sensor")
    
    
    APP.run()
