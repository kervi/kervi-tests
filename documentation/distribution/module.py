if __name__ == '__main__':
    from kervi.module import Module
    APP_MODULE = Module()

    from kervi.sensors.sensor import Sensor
    from kervi.devices.platforms.common.sensors.cpu_use import CPULoadSensorDeviceDriver

    SENSOR_1 = Sensor("module_cpu_load", "Module CPU", CPULoadSensorDeviceDriver())
    SENSOR_1.link_to_dashboard(type="value", link_to_header=True)
    SENSOR_1.link_to_dashboard(type="chart")

    APP_MODULE.actions.shutdown.link_to_dashboard("*", "header_right", inline=True, label=None, button_text="Module shutdown")

    APP_MODULE.run()    
