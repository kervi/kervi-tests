if __name__ == '__main__':
    from kervi.bootstrap import Application
    APP = Application()

    #add dashboard and panel
    from kervi.dashboard import Dashboard, DashboardPanel
    DASHBOARD = Dashboard("dahsboard.app", "Test BMP085", is_default=True)
    DASHBOARD.add_panel(DashboardPanel("sensor", columns=2, rows=4, title=None))
    
    from kervi.sensor import Sensor
    from kervi_devices.sensors import BMP085
    SENSOR_TEMP = Sensor("BMP085_temp", "Temperature", BMP085.BMP085DeviceDriver(BMP085.BMP085_TEMPERATURE_SENSOR))
    SENSOR_TEMP.link_to_dashboard("dashboard.app", "sensor")

    SENSOR_PRESSURE = Sensor("BMP085_pressure", "Pressure", BMP085.BMP085DeviceDriver(BMP085.BMP085_TEMPERATURE_SENSOR))
    SENSOR_PRESSURE.link_to_dashboard("dashboard.app", "sensor")

    SENSOR_ALTITUDE = Sensor("BMP085_altitude", "Altitude", BMP085.BMP085DeviceDriver(BMP085.BMP085_TEMPERATURE_SENSOR))
    SENSOR_ALTITUDE.link_to_dashboard("dashboard.app", "sensor")
    
    APP.run()