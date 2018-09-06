if __name__ == '__main__':
    from kervi.application import Application
    APP = Application()

    #add dashboard and panel
    
    from kervi.sensors.sensor import Sensor
    import kervi.devices.sensors.BMP085 as BMP085
    SENSOR_TEMP = Sensor("BMP085_temp", "Temperature", BMP085.BMP085DeviceDriver(BMP085.BMP085_TEMPERATURE_SENSOR))
    SENSOR_TEMP.link_to_dashboard()

    SENSOR_PRESSURE = Sensor("BMP085_pressure", "Pressure", BMP085.BMP085DeviceDriver(BMP085.BMP085_PRESSURE_SENSOR))
    SENSOR_PRESSURE.link_to_dashboard()

    SENSOR_ALTITUDE = Sensor("BMP085_altitude", "Altitude", BMP085.BMP085DeviceDriver(BMP085.BMP085_ALTITUDE_SENSOR))
    SENSOR_ALTITUDE.link_to_dashboard()

    APP.run()