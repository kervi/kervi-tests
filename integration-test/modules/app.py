if __name__ == '__main__':
    from kervi.application import Application
    APP = Application(
        
    )

    #add dashboard and panel
    from kervi.dashboards import Dashboard, DashboardPanel
    DASHBOARD = Dashboard("dashboard.app", "app dashboard", is_default=True)
    DASHBOARD.add_panel(DashboardPanel("cpu", columns=2, rows=4, title=None))


    from kervi.sensors.sensor import Sensor
    from kervi.devices.platforms.common.sensors.cpu_use import CPULoadSensorDeviceDriver
    SENSOR_1 = Sensor("CPULoadSensor", "CPU", CPULoadSensorDeviceDriver())
    #link to sys area top right
    SENSOR_1.link_to_dashboard("*", "sys-header")
    #link to a panel, show value in panel header and chart in panel body
    SENSOR_1.link_to_dashboard("dashboard.app", "cpu", type="value", size=2, link_to_header=True)
    SENSOR_1.link_to_dashboard("dashboard.app", "cpu", type="chart", size=2)

    APP.actions.shutdown.link_to_dashboard("*", "header_right", inline=True, label=None, button_text="App shutdown")

    
    APP.run()