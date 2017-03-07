if __name__ == '__main__':
    from kervi.bootstrap import Application
    APP = Application()

    #add dashboard and panel
    from kervi.dashboard import Dashboard, DashboardPanel
    DASHBOARD = Dashboard("dashboard.app", "Test BMP085", is_default=True)
    DASHBOARD.add_panel(DashboardPanel("sensor", columns=2, rows=4, title=None))

    from kervi.hal import GPIO
    from kervi.sensor import Sensor
    from kervi_devices.sensors import TSL2561
    
    SENSOR = Sensor("TSL2561", "Light", TSL2561.TSL2561SDeviceDriver())
    SENSOR.link_to_dashboard("dashboard.app", "sensor")

    
    APP.run()