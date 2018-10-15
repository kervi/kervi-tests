if __name__ == '__main__':
    from kervi.application import Application
    APP = Application()

    
    from kervi.hal import GPIO
    from kervi.sensors import Sensor
    from kervi.devices.sensors.TCS34725 import TCS34725DeviceDriver

    SENSOR = Sensor("color", "Color", TCS34725DeviceDriver())
    SENSOR.link_to_dashboard()
    
    APP.run()