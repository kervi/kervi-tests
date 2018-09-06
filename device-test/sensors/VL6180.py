if __name__ == '__main__':
    from kervi.application import Application
    APP = Application()

    #add dashboard and panel
    
    from kervi.sensors.sensor import Sensor
    from kervi.devices.sensors.VL6180X import VL6180DistanceDeviceDriver, VL6180LuxDeviceDriver
    sensor = Sensor("vl6180x_distnace", "Distance", VL6180DistanceDeviceDriver())
    sensor.link_to_dashboard()

    sensor1 = Sensor("vl6180x_lux", "lux", VL6180LuxDeviceDriver())
    sensor1.link_to_dashboard()


    APP.run()