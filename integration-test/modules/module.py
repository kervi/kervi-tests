import kervi.utility.nethelper as nethelper

if __name__ == '__main__':
    from kervi.bootstrap import ApplicationModule
    APP_MODULE = ApplicationModule({
        "info":{
            "id":"module.id",
            "name":"Module name"
        },
        "log":{
            "file":"kervi-module.log"
        },
        "network":{
            "IPAddress": nethelper.get_ip_address(),
            "IPRootAddress": "192.168.0.21",
            "IPCRootPort": 9500,
        }
    })

    from kervi.dashboard import Dashboard, DashboardPanel
    DASHBOARD = Dashboard("dashboard.module", "module dashboard", is_default=True)
    DASHBOARD.add_panel(DashboardPanel("panel", columns=2, rows=2, title="Panel dashboard"))


    from kervi.sensor import Sensor
    from kervi_devices.platforms.common.sensors.memory_use import MemUseSensorDeviceDriver
    SENSOR_1 = Sensor("MemLoadSensor", "MEM", MemUseSensorDeviceDriver())
    #link to sys area top right
    SENSOR_1.link_to_dashboard("*", "sys-header")
    #link to a panel, show value in panel header and chart in panel body
    SENSOR_1.link_to_dashboard("dashboard.module", "panel", type="value", size=2, link_to_header=True)
    SENSOR_1.link_to_dashboard("dashboard.module", "panel", type="chart", size=2)



    APP_MODULE.run()