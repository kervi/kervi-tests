# Copyright (c) 2016, Tim Wentzlau
# Licensed under MIT

if __name__ == '__main__':
    from kervi.bootstrap import Application
    from kervi import tasks
    APP = Application()

    #add dashboard and panel
    from kervi.dashboard import Dashboard, DashboardPanel
    DASHBOARD = Dashboard("system", "Sensor test", is_default=True)
    DASHBOARD.add_panel(DashboardPanel("multi_sensor", columns=3, rows=4, title="Multi sensor"))
    DASHBOARD.add_panel(DashboardPanel("multi_sensor_single", columns=3, rows=4, title="Multi sensor single"))
    DASHBOARD.add_panel(DashboardPanel("gauge", columns=3, rows=4, title="Gauge"))
    DASHBOARD.add_panel(DashboardPanel("log", columns=3, rows=4, title="Log", user_log=True))

    from kervi.sensor import Sensor
    from kervi_devices.platforms.common.sensors.cpu_use import CPULoadSensorDeviceDriver
    from kervi_devices.sensors.dummy_sensor import DummyMultiDimSensorDeviceDriver

    cpu_sensor = Sensor("CPULoadSensor","CPU", CPULoadSensorDeviceDriver())
    cpu_sensor.store_to_db = False
    cpu_sensor.link_to_dashboard("*", "sys-header")
    cpu_sensor.link_to_dashboard("system", "cpu", type="value", size=2, link_to_header=True)
    cpu_sensor.link_to_dashboard("system", "cpu", type="chart", size=2)


    multi_sensor = Sensor("MultiSensor", "multi sensor", DummyMultiDimSensorDeviceDriver())
    multi_sensor.store_to_db = False
    multi_sensor.link_to_dashboard("system", "multi_sensor", type="value", size=1)

    multi_sensor[0].link_to_dashboard("system", "multi_sensor_single", type="value", size=2)
    multi_sensor[1].link_to_dashboard("system", "multi_sensor_single", type="value", size=2)
    multi_sensor[2].link_to_dashboard("system", "multi_sensor_single", type="value", size=2)

    multi_sensor[0].link_to_dashboard("system", "gauge", type="horizontal_linear_gauge", size=2)
    multi_sensor[1].link_to_dashboard("system", "gauge", type="vertical_linear_gauge", size=2)

    multi_sensor[2].add_error_range((0, 10), "l error message")
    multi_sensor[2].add_warning_range((10, 20), "l warning message")
    multi_sensor[2].add_warning_range((80, 90), "h warning message")
    multi_sensor[2].add_error_range((90, 100), "h error message")
    multi_sensor[2].link_to_dashboard("system", "gauge", type="radial_gauge", size=1)

    APP.run()
