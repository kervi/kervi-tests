if __name__ == '__main__':

    from kervi.application import Application
        
    app = Application()

    from kervi.sensors import Sensor
    from kervi.devices.sensors.system import CPULoadSensorDeviceDriver

    cpu_load_sensor = Sensor("CPULoadSensor","CPU", CPULoadSensorDeviceDriver())
    cpu_load_sensor.link_to_dashboard("*", "header_right")
    cpu_load_sensor.link_to_dashboard(type = "value", show_sparkline=True, link_to_header=True)
    cpu_load_sensor.link_to_dashboard(type="chart")

    app.run()