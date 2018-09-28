if __name__ == '__main__':
    from kervi.application import Application
    APP = Application()

    from kervi.sensors.sensor import Sensor
    from kervi.devices.sensors.CW2015 import CW2015VoltageDeviceDriver, CW2015CapacityDeviceDriver
    
    sensor = Sensor("CW2015_voltage", "CW2015 voltage", CW2015VoltageDeviceDriver())
    sensor.link_to_dashboard()

    sensor1 = Sensor("CW2015_capacity", "CW2015 capacity", CW2015CapacityDeviceDriver())
    sensor1.link_to_dashboard()

    APP.actions.shutdown.link_to(sensor1, trigger_value= lambda x: x<50)

    APP.run()