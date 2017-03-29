if __name__ == '__main__':
    from kervi.bootstrap import Application
    APP = Application()

    #add dashboard and panel
    from kervi.dashboard import Dashboard, DashboardPanel
    DASHBOARD = Dashboard("dashboard.app", "Test BMP085", is_default=True)
    DASHBOARD.add_panel(DashboardPanel("sensor", columns=2, rows=4, title=None))

    from kervi.hal import GPIO
    from kervi.sensor import Sensor
    from kervi_devices.sensors import LSM9DS0

    SENSOR_COMPASS = Sensor("compass", "Compass", LSM9DS0.LSM9DS0CompasDeviceDriver())
    SENSOR_COMPASS.link_to_dashboard("dashboard.app", "sensor")

    APP.run()