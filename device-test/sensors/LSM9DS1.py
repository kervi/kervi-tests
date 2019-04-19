if __name__ == '__main__':
    from kervi.application import Application
    APP = Application()

    #add dashboard and panel
    from kervi.dashboards import Dashboard, DashboardPanel
    DASHBOARD = Dashboard("dashboard.app", "Test LSM9DS1.py", is_default=True)
    DASHBOARD.add_panel(DashboardPanel("accl", title="Acceleration"))
    DASHBOARD.add_panel(DashboardPanel("gyro", title="Gyro"))
    DASHBOARD.add_panel(DashboardPanel("magnetic", title="Magnetic"))

    from kervi.hal import GPIO
    from kervi.sensors import Sensor
    
    import kervi.devices.sensors.LSM9DS1 as LSM9DS1

    SENSOR_ACCL = Sensor("accl", "Acceleration", LSM9DS1.LSM9DS1AccelerationDeviceDriver())
    SENSOR_ACCL.link_to_dashboard("dashboard.app", "accl")

    SENSOR_GYRO = Sensor("gyro", "gyro", LSM9DS1.LSM9DS1GyroDeviceDriver())
    SENSOR_GYRO.link_to_dashboard("dashboard.app", "gyro")

    SENSOR_MAG = Sensor("magnetic", "Magnetic", LSM9DS1.LSM9DS1MagneticDeviceDriver())
    SENSOR_MAG.link_to_dashboard("dashboard.app", "magnetic")

    APP.run()
