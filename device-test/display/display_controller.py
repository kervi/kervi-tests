if __name__ == '__main__':
    from kervi.application import Application
    APP = Application({
        "unit_system":  "us-imperial",
        "network":{
            "ip": "127.0.0.1",
            "ipc_root_address": "127.0.0.1"
        }

    })


    from kervi.sensors import Sensor
    from kervi.devices.sensors.system import CPULoadSensorDeviceDriver
    from kervi.devices.sensors.system import CPUTempSensorDeviceDriver
    from kervi.devices.sensors.dummy_sensor import DummySensorDeviceDriver
    #build in sensor that measures cpu use
    SENSOR_CPU_LOAD = Sensor("CPULoadSensor", "CPU", CPULoadSensorDeviceDriver())
    #link to sys area top right
    SENSOR_CPU_LOAD.link_to_dashboard("*", "sys-header")
    #link to a panel, show value in panel header and chart in panel body
    SENSOR_CPU_LOAD.link_to_dashboard(type="value", size=2, link_to_header=True)
    SENSOR_CPU_LOAD.link_to_dashboard(type="chart", size=2)

    #build in sensor that measures cpu temperature
    SENSOR_CPU_TEMP = Sensor("CPUTempSensor", "", DummySensorDeviceDriver(type="temperature", unit="c"))
    #link to sys area top right
    SENSOR_CPU_TEMP.link_to_dashboard("*", "sys-header")


    from kervi.devices.displays.dummy_display_driver import DummyCharDisplayDriver, DummyBitmapDisplayDriver
    from kervi.devices.displays.SSD1306 import SSD1306DeviceDriver
    from kervi.displays import Display, DisplayPage

    page1 = DisplayPage("p1")
    page1.template = "CPU: {CPULoadSensor}%\nLine 2\nline 3 æøåäð"
    page1.link_value(SENSOR_CPU_LOAD, "2.0f")

    page2 = DisplayPage("p2")
    page2.template = "temp: {CPUTempSensor} {CPUTempSensor_unit}\nx"
    page2.link_value(SENSOR_CPU_TEMP, "3.1f")


    page3 = DisplayPage("p3")
    page3.template = "xabcæøåÆØÅ"

    display = Display("d1", "Display", DummyCharDisplayDriver())
    display.text.link_to_dashboard()
    display.add_page(page2)

    # display1 = Display("d2", "Display 2", SSD1306DeviceDriver(32))
    # display1.text.link_to_dashboard()
    # display1.add_page(page1)
    # display1.add_page(page2)
    # display1.add_page(page3)
    # display1.activate_page_scroll()


    APP.run()
