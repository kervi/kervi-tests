if __name__ == '__main__':
        from kervi.application import Application
        APP = Application()

        from kervi.sensors.sensor import Sensor
        from kervi.devices.platforms.common.sensors.cpu_use import CPULoadSensorDeviceDriver

        SENSOR_1 = Sensor("app_CPULoadSensor", "App CPU", CPULoadSensorDeviceDriver())
        SENSOR_1.link_to_dashboard(type="value", link_to_header=True)
        SENSOR_1.link_to_dashboard(type="chart")

        APP.actions.shutdown.link_to_dashboard("*", "header_right", inline=True, label=None, button_text="App shutdown")

        APP.run()