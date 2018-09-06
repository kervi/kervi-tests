if __name__ == '__main__':
    from kervi.application import Application
    APP = Application()

    #add dashboard and panel
    from kervi.dashboards import Dashboard, DashboardPanel
    
    from kervi.sensors.sensor import Sensor
    from kervi.devices.sensors.TSL2561 import TSL2561DeviceDriver
    
    SENSOR = Sensor("TSL2561", "Light", TSL2561DeviceDriver())
    SENSOR.link_to_dashboard()

    
    APP.run()